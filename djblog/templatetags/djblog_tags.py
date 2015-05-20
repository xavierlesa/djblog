# *-* coding=utf-8 *-*

from django.db.models import Q, F
from django.db.models.query import QuerySet
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import striptags
from markdown import markdown

from djblog.models import Post, Tag, Category

register = template.Library()

################################################################################
# tags new style
################################################################################
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify, striptags, truncatewords, truncatechars, force_escape, escape, date

import logging
logger = logging.getLogger(__name__)

import django
DJANGO_VERSION = [i for i in django.get_version().split('.')]

if DJANGO_VERSION <= [1,4,5]:
    try:
        from django.template import add_to_builtins
        add_to_builtins('djblog.templatetags.getblog')
    except ImportError:
        logger.warning("Esta version de django (%s) no acepta add_to_builtins", django.get_version())
else:
    logger.warning("Esta version de django (%s) no acepta add_to_builtins, `getblog` debe cargarse a manopla", django.get_version())


# get title for post
@register.simple_tag(takes_context=True)
def post_title(context, *args, **kwargs):
    """
    Devuelve el título de un post/pagina
    {% post_title %}
    Por defecto post_title resuelve el object desde el contexto, pero es posible 
    pasar uno desde los argumentos.
    {% post_title [object=post [limit=12]] %}
    Es posible limitar la cantidad de caracteres pasando el argumento limit.
    """
    obj = context['object']
    if kwargs.get('limit'):
        return obj.title[:kwargs['limit']]
    return obj.title

# get first image for post
@register.simple_tag(takes_context=True)
def post_image(context, *args, **kwargs):
    """
    Devuelve la imagen principal asociada al post/page
    {% post_image [size=[320x200|thumbnail|gallery] attrs="class='thumb'"] %}
    No tiene ningún argumento obligatorio, pero si es posible modificar el 
    tamaño y los atributos del tag.
    size: thumbnail y gallery son valores predefinidos pero sino puede ser 
    seteado con width x height, así 320x200.
    attrs: Son pasados cómo vienen al tag <img src=... %(attrs)s/>
    """
    from mediacontent.models import MediaContent
    obj = context['object']
    fallback = "%s%s" % (settings.STATIC_URL, kwargs.get('placeholder')) if kwargs.has_key('placeholder') else ''

    if kwargs.has_key('save'):
        context[kwargs['save']] = ''

    if not obj:
        return '<img src="%s" />' % fallback
    attrs = kwargs.get('attrs', '') 
    size = kwargs.get('size', 'content') # size can be [width]x[height] autocrop :)
    img = None
    if isinstance(obj, MediaContent):
        img = obj
    elif kwargs.has_key('title'):
        iqs = obj.media_content.filter(mimetype__startswith="image", title=kwargs['title'])
        if iqs.exists():
            img = iqs[0]
    else:
        img = obj.get_first_image()

    if not img or not isinstance(img, MediaContent) or not img.content:
        if fallback:
            return mark_safe('<img src="%s" %s />' % (fallback, attrs))
        else:
            return ''
    
    if size == 'gallery' and img.gallery:
        img_url = img.gallery.url
    elif size == 'thumbnail' and img.thumbnail:
        img_url = img.thumbnail.url
    elif len(size.split('x')) == 2:
        width, height = size.split('x')
        content_path = img.content.path.split('.')
        content_url = img.content.url.split('/')
        crop_path = '%s_%s.%s' % (''.join(content_path[:-1]), size, content_path[-1])
        crop_url = '%s/%s' % ('/'.join(content_url[:-1]), crop_path.split('/')[-1])
        try:
            with open(crop_path):
                pass
        except IOError:
            from PIL import Image, ImageOps
            try:
                image = Image.open(img.content.path)
                thumb = ImageOps.fit(image, [int(x) for x in size.split('x')], 0, Image.ANTIALIAS, (0.5, 0.0))
                thumb.save(crop_path, 'JPEG', quality=90)
            except IOError:
                img_alt = "imagen no disponible"
                img_title = img_alt
                img_url = "http://placehold.it/%sx%s&text=%s" % (width, height, img_title)
                img_tag = "<!-- no disponible %(origin_src)s --><img src=\"%(src)s\" %(attrs)s alt=\"%(alt)s\" title=\"%(title)s\"/>"
                return mark_safe(img_tag % {'origin_src':img.content.path, 'src': img_url, 'alt': img_alt, 'title': img_title, 'attrs': attrs })

        img_url = crop_url
    else:
        img_url = img.content.url

    img_alt = img.content.name
    img_title = img.title or obj.title
    img_tag = "<img src=\"%(src)s\" %(attrs)s alt=\"%(alt)s\" title=\"%(title)s\"/>"
    if kwargs.get('just_url', False):
        return img_url
    result = mark_safe(img_tag % {'src': img_url, 'alt': img_alt, 'title': img_title, 'attrs': attrs })
    if kwargs.has_key('save'):
        context[kwargs['save']] = result
        return '<!---->'
    return result

# the extract
@register.simple_tag(takes_context=True)
def post_extract(context, *args, **kwargs):
    """
    Genera el extracto a partir del contenido.
    {% post_extract %}
    Por defecto post_extract resuelve el object desde el contexto, pero es 
    posible pasar uno desde los argumentos.
    {% post_extract object=post [limit=40 [limit_chars=200]] %}
    Por defecto limita a 30 palabras, pero es posible pasar los argumentos limit 
    o limir_chars para controlar los límites.
    """
    obj = context['object']
    limit = kwargs.get('limit', 30)
    limit_chars = kwargs.get('limit_chars', 0)
    if not obj:
        return ''

    data = obj.first_paragraph['content'] if obj.first_paragraph else obj.content

    if kwargs.get('markdown', False):
        data = markdown(data)

    if not kwargs.get('safe', False):
        data = striptags(data)

    if limit_chars:
        return truncatechars(data, limit_chars)
    return truncatewords(data, limit)

# date of post
@register.simple_tag(takes_context=True)
def post_date(context, *args, **kwargs):
    """
    Retorna la fecha el post/page publication_date.
    {% post_date [format="l j, F"] %}
    User los siguientes formatos https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
    """
    obj = context['object']
    date_format = kwargs.get('format', "l j, F")
    return date(obj.publication_date, date_format)


# the content
@register.simple_tag(takes_context=True)
def post_content(context, *args, **kwargs):
    """
    Retorna el contenido renderizado del post/page content_render
    {% post_content %}
    """
    obj = context['object']
    content = obj.content_rendered
    return mark_safe(content)


# the archive
@register.assignment_tag()
def post_archive(*args, **kwargs):
    """
    Retorna un QuerySet con el "Archivo" de los post/page por meses.
    <ul>
    {% post_archive as archive_list %}
    {% for archive in archive_list %}
    <li><a href="{{ archive.get_absolute_url }}">{{ archive }}</a></li>
    {% endfor %}
    </ul>
    """
    return Post.objects.dates('publication_date', 'month')
    

@register.filter
def post_video(obj, key=None):
    try:
        vid = obj.get_extra_content().filter(key='video')[0]
        ret = json.loads(vid.field)
        if key:
            ret = ret[key]
        return ret
    except:
        try:
            parsed_content = obj.parse_content()
            if parsed_content:
                for row in parsed_content:
                    for obj in row:
                        if obj['type'] == 'video:youtube':
                            return obj['content']
        except:
            pass
    return ''

@register.assignment_tag
def get_pages_from_category(cat, recursive=None):
    """
    Devuelve el QuerySet de page para una categoría.
    {% get_pages_from_category cat=category-slug [recursive=recursive] as object_list %}
    Si se quiere incluir las categorías childs hay que agregar el argumento 
    recursive=recursive
    """
    qs = Post.objects.get_pages()
    if recursive == 'recursive':
        qs = qs.filter(Q(category__slug=cat) | Q(category__parent__slug=cat))
    else:
        qs = qs.filter(category__slug=cat)
    return qs.distinct()


# TODO: deberiamos cambiarlo a get_posts_from_category
@register.assignment_tag
def get_from_category(cat, recursive=None):
    """
    Devuelve el QuerySet de post para una categoría.
    {% get_posts_from_category cat=category-slug [recursive=recursive] as object_list %}
    Si se quiere incluir las categorías childs hay que agregar el argumento 
    recursive=recursive
    """
    if recursive == 'recursive':
        qs = Post.objects.public().filter(Q(category__slug=cat) | Q(category__parent__slug=cat))
    else:
        qs = Post.objects.public().filter(category__slug=cat)
    return qs.distinct()

register.assignment_tag(name='get_posts_from_category')(get_from_category)

@register.assignment_tag
def get_post_or_page(slug=None, id=None):
    """
    Retorna un post o page por slug o ID
    {% get_post_or_page [id=23|slug=acerca-de] as object %}
    """
    if id:
        try:
            return Post.objects.public().get(id=id)
        except Post.DoesNotExist:
            pass

    elif slug:
        try:
            return Post.objects.public().get(slug=slug)
        except Post.DoesNotExist:
            pass

    return ''


@register.filter
def get_post_extra_content_key_name(obj, key_name=None):
    """
    Devuelve los extra_content asociados al post/page filtrando por key y name
    {{ object|get_post_extra_content_key_name:'pdf:attached' }}
    """
    if obj:
        key, name = key_name.split(',')
        return obj.get_extra_content().filter(key__iexact=key, name__iexact=name)
    return ''


@register.filter
def get_post_extra_content_key(obj, key_name=None):
    """
    Devuelve los extra_content asociados al post/page filtrando por key
    {{ object|get_post_extra_content_key:'pdf' }}
    """
    return obj.get_extra_content().filter(key__iexact=key_name)


@register.filter
def get_post_extra_content_by_keys(obj, keys=None):
    """
    Devuelve los extra_content asociados al post/page filtrando por mas de una key
    {{ object|get_post_extra_content_by_keys:'pdf,doc,txt' }}    
    """
    key = keys.split(',')
    return obj.get_extra_content().filter(key__in__iexact=key)


@register.assignment_tag
def get_category(slug):
    """
    Retorna una category por slug
    {% get_category slug=category-name as object %}
    """
    try:
        return Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        pass
    return ''

@register.assignment_tag
def get_all_categories(slug=None, blog=False, children=False, recursive=False, max_level=2):
    """
    Retorna el `QuerySet` de Category según algunos filtros.
    Si el `slug` está presente filtra por aquellas `Category` que tengan como
    parent este `slug`.
    Si el `slug` y `children` es `True` también filtra por aquellas que también
    tengan este `slug`, es decir filtra por aquellas que tengan el `slug` como 
    child o parent.
    El argumento `blog` filtra el `QuerySet` por `Category` de `blog`, con el 
    flag `blog_category=True`.
    `recursive` busca de forma recursiva la conincidencia del `slug` con un máximo
    de 2 niveles por defecto, pero se puede ajustar desde `max_level`.
    """
    qs = Category.objects.active()
    
    if slug:
        query = Q(parent__slug=slug)
        if not children:
            query = query | Q(slug=slug)
        if recursive:
            while max_level > 0:
                k = "%s__slug" % '__'.join(['parent'] * max_level)
                query = query | Q(**{k: slug})
                max_level -= 1
                
        qs = qs.filter(query)
    
    if blog:
        qs = qs.filter(blog_category=True)
    
    return qs

@register.assignment_tag(takes_context=True)
def get_sub_categories(context, slug):
    """
    Retorna las category del post/page donde el parent es el slug del argumento.
    {% get_sub_categories slug=category-name as object_list %}
    """
    obj = context.get('object', False)
    if obj:
        return obj.category.filter(parent__slug=slug)
    return ''


@register.assignment_tag
def get_tags_list(*args, **kwargs):
    """
    Retorna todos los `tags` acumulados 
    {% get_tags_list as object_list %}
    """
    return Tag.objects.active()


@register.assignment_tag
def get_posts_for_tags(slug=None, id=None, *args, **kwargs):
    """
    Filtra por `taxonomia` los `post` con los `tags` asociados
    {% get_posts_for_tags [tags='perro,gato,liebre'] [id='1,34,56'] [<Tag: object>] [<Tag QuerySet>] as object_list %}
    """
    if slug and isinstance(slug, basestring):
        tags = slug.split(',')
        qs = Post.objects.filter(tags__slug__in=tags)
    elif slug and isinstance(slug, (QuerySet, Tag)):
        qs = Post.objects.filter(tags__in=slug) 
    elif id and isinstance(id, basestring):
        ids = id.split(',')
        qs = Post.objects.filter(tags__id__in=ids) 
    else:
        qs = Post.objects.none()
    return qs


def get_tags_list(*args, **kwargs):
    """
    Retorna todos los `tags` acumulados 
    {% get_tags_list as object_list %}
    """
    return Tag.objects.active()


@register.filter
def get_columns(qs, cols):
    """
    deprecated/obsoleto
    """
    return len(qs) / cols

@register.filter
def extract(obj, splitter='<!--more-->'):
    """
    Devuelve el contenido del post/page partido por el splitter
    {{ object|extract:'<!--more-->' }}
    """    
    return obj.split(splitter)

@register.filter
def has_category(obj, cat):
    """
    Retorna True si la categoría está asociada al post/page
    {{ object|has_category:'slug-of-category' }}
    """
    if obj.category.filter(slug=cat).exists():
        return True
    return False


@register.filter
def exclude_object(qs, obj):
    return qs.exclude(pk=obj.pk)
