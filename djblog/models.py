# -*- coding:utf-8 -*-
"""
Una app para hacer un simple blog, con posts, páginas y blocks

"""
import collections

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
import logging
logger = logging.getLogger(__name__)

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import *
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.timezone import now as tz_now, get_current_timezone, utc

from mediacontent.models import MediaContent

from djblog.content_extra.models import ExtraContent, ContentType
from djblog.managers import TagManager, CategoryManager, PostManager
from djblog.common.models import BaseModel, ContentModel, CategoryModel, CustomTemplate

DJBLOG_PREVIEW_CONTENT_SIZE = getattr(settings, 'DJBLOG_PREVIEW_CONTENT_SIZE', 45)
DJBLOG_CONTENT_FORMAT = getattr(settings, 'DJBLOG_CONTENT_FORMAT', 'html') # plain = plano, html
DJBLOG_LAYOUT_TEMPLATE = getattr(settings, 'DJBLOG_LAYOUT_TEMPLATE', 
    (
        ('1col', '1 columna'), 
        ('2col', '2 columnas'),
        ('3col', '3 columnas'),
    )
)
DJBLOG_DEFAULT_POST_URL_NAME = getattr(settings, 'DJBLOG_DEFAULT_POST_URL_NAME', 'blog_detail')
DJBLOG_GENERIC_POST_DETAIL_URL_NAME = getattr(settings, 'DJBLOG_GENERIC_POST_DETAIL_URL_NAME', 'generic_post_detail')
DJBLOG_GENERIC_POST_LIST_URL_NAME = getattr(settings, 'DJBLOG_GENERIC_POST_LIST_URL_NAME', 'generic_post_list')

class Tag(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    objects = TagManager()

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return (u'blog_tag_list', (self.slug,))

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _(u"Etiquetas")
        verbose_name = _(u"Etiqueta")


class Status(models.Model):
    name = models.CharField(max_length=140, verbose_name=_(u"Nombre o Título"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    is_public = models.BooleanField(default=False, blank=True, 
            help_text=_(u"Este estado determina si una publicación es visible o no"))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _(u"Estados")
        verbose_name = _(u"Estado")


class Category(BaseModel, CategoryModel):
    blog_category = models.BooleanField(default=True, blank=True)
    description = models.TextField(blank=True, null=True)
    show_on_list = models.BooleanField(default=False)
    objects = CategoryManager()
    parent = models.ManyToManyField('self', symmetrical=False, through='CategoryRelationship',
                                    null=True, blank=True, related_name='children')

    def __unicode__(self):
        return u"%s > %s" % (self.name, self.level)

    @models.permalink
    def get_absolute_url(self):
        if self.blog_category:
            return (u'blog_category_list', (self.slug,))
        else:
            return (u'page_category_list', (self.slug,))

    def get_category_childs(self):
        # todo las categorías childs
        cc = []
        for cat in Category.objects.filter(parent__in=[self]):
            cc.append(cat)
            child = cat.get_category_childs()
            if child:
                cc.append(child)
        return cc

    def get_root_category(self):
        if self.parent:
            p = self.parent
            while True:
                if not p.parent: break
                p = p.parent
            return p
        else:
            return self

    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, 'create_new_slug'):
                self.slug = self.create_new_slug()
            else:
                self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    #def save(self, *args, **kwargs):
    #    """Set up root_leve and slug"""

    #    if self.parent.all() != 0:
    #        self.level = self.parent.first().level + 1
    #        self.blog_category = self.parent.first().blog_category

    #    super(Category, self).save(*args, **kwargs)
 
    class Meta:
        ordering = ('level', '-pub_date', 'name', )
        verbose_name_plural = _(u"Categorías")
        verbose_name = _(u"Categoría")


class CategoryRelationship(models.Model):
    from_category = models.ForeignKey(Category, related_name="from_category")
    to_category = models.ForeignKey(Category, related_name="to_category")

    
    def save(self, *args, **kwargs):
        super(CategoryRelationship, self).save(*args,**kwargs)

        if self.from_category.level != self.to_category.level + 1:
            self.from_category.level = self.to_category.level + 1
            self.from_category.save()


# NEW: Ahora se puede elegir el tipo de contenido e impacta en cómo se va a 
# usar la URL y los tempaltes, así se pueden customizar aun más

class PostType(CustomTemplate, BaseModel):
    post_type_name = models.CharField(_(u"Tipo de objeto"), max_length=100, 
            help_text=_(u"Determina el uso y comportamiento del Post, \n\
                    siendo `Post` y `Página` los reservados y por defecto."))

    post_type_slug = models.SlugField(_(u"Slug del tipo"), 
            help_text=_(u"Importante para determinar el inicio de URL. \n\
                    Ej: Para el `slug` `autos` \n\
                    /post_type_slug/slug/ -> /autos/peugeot-208/"))

    def __unicode__(self):
        return self.post_type_name

    @property
    def is_page(self):
        return self.post_type_slug == 'page'

    @property
    def is_blog(self):
        return self.post_type_slug == 'blog'

    @models.permalink
    def get_absolute_url(self):
        return (DJBLOG_GENERIC_POST_LIST_URL_NAME, (), {
            'post_type_slug': self.post_type_slug, 
            })

    def get_media_content(self):
        return MediaContent.objects.get_for_model(self)
    media_content = property(get_media_content)

    def get_extra_content(self, *args, **kwargs):
        return ExtraContent.objects.get_for_model(self)
    extra_content = property(get_extra_content)


class Post(CustomTemplate, BaseModel, ContentModel):
    """
    Post o Página

    title, copete, content, content_rendered
    """
    #is_page = models.BooleanField(default=False, blank=True, 
    #        choices=(
    #            (False, u"Post"),
    #            (True, u"Página")
    #        ), 
    #        verbose_name=_(u"Tipo de posteo"))

    post_type = models.ForeignKey(PostType)

    publication_date = models.DateTimeField(verbose_name=_(u"Fecha de publicación"))
    expiration_date = models.DateTimeField(blank=True, null=True, 
            verbose_name=_(u"Fecha de vencimiento"))

    category = models.ManyToManyField(Category, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True)
    sort_order = models.PositiveIntegerField(_(u'Orden'),default=1) 

    tags = models.ManyToManyField(Tag, blank=True, help_text=_(u"Tags descriptívos"))

    # Deprecado, nunca se usó
    #followup_for = models.ManyToManyField('self', symmetrical=False, blank=True, 
    #        related_name='followups', verbose_name=_(u"Contenido sugerido"))

    related = models.ManyToManyField('self', blank=True, 
            verbose_name=_(u"Contenido relacionado"))

    allow_comments = models.NullBooleanField(blank=True, null=True, default=True, 
            verbose_name=_(u"Permitir comentarios")) # por defecto permite comentarios

    comments_finish_date = models.DateTimeField(blank=True, null=True, 
            verbose_name=_(u"Cerrar automáticamente"))


    objects = PostManager()

    class Meta:
        get_latest_by = 'publication_date'
        ordering = ('-sort_order', '-publication_date', 'title')
        verbose_name_plural = _(u"Posts")
        verbose_name = _(u"Post")

    @models.permalink
    def get_absolute_url(self):
        """
        Resuelve la URL para un objeto
        """

        # es una página
        #if self.is_page:
        if self.post_type.is_page:
            # es un post noblog
            if self.category.all():
                category = self.get_tree_category()
                if category:
                    return (u'page_hierarchy_detail', [], {
                        'category_slug': category.slug, 
                        'hierarchy_slug':self.slug
                    })
            
            return (u'page_detail', (self.slug,))

        elif self.post_type.is_blog:
            if DJBLOG_DEFAULT_POST_URL_NAME == 'blog_detail':
                pub_date = self.publication_date.strftime('%Y %m %d').split()
                pub_date.append(self.slug)
                return ('blog_detail', pub_date)

            return (DJBLOG_DEFAULT_POST_URL_NAME, (), {'slug':self.slug})

        # URL genérica para los demas tipos de objetos
        # /post_type_slug/slug/
        return (DJBLOG_GENERIC_POST_DETAIL_URL_NAME, (), {
            'post_type_slug': self.post_type.post_type_slug, 
            'slug':self.slug
            })


    def save(self, *args, **kwargs):
        # fix error del prepopulated
        # usa la funcion create_new_slug para evitar duplicacion a la hora de corregir el slug
        if not self.slug:
            self.slug = self.create_new_slug()

        #if not self.content:
        #    self.content = self.content_rendered
        # auto-genera los meta
        if not self.meta_description or self.meta_description != self.content.replace('"',''):
            self.meta_description = self.content.replace('"','')

        if not self.pub_date:
            self.pub_date = tz_now()
        if not self.publication_date:
            self.publication_date = self.pub_date

        return super(Post, self).save(*args, **kwargs)

    def get_root_category(self):
        category = self.category.filter(level__gte=0)
        if category:
            return category[0].get_root_category()
        return []

    def get_tree_category(self):
        """
        Devuelve todo el árbol de cateogiras, siendo el mas "largo" el por defecto,
        y ordenado alfabéticamente.
        """
        category = self.category.all().order_by('level')[0]
        return category
    
    def get_preview_content(self):
        return mark_safe(truncatewords_html(self.content_rendered, DJBLOG_PREVIEW_CONTENT_SIZE))
    preview_content = property(get_preview_content)

    def get_first_thumb_url(self):
        content = self.first_content
        if content:
            if hasattr(content, 'gallery') and hasattr(content.gallery, 'url'):
                return content.gallery.url
            elif hasattr(content, 'field_json') and content.field_json.has_key('thumb'):
                return content.field_json['thumb']
        return ''
    first_thumb_url = property(get_first_thumb_url)

    def get_first_content(self):
        images = MediaContent.objects.get_for_model(self).filter(mimetype__startswith='image')
        if images:
            return images[0]
        else:
            extra = ExtraContent.objects.get_for_model(self).filter(key__in=['video','image'])
            if extra:
                return extra[0]
    first_content = property(get_first_content)

    def get_media_content(self):
        return MediaContent.objects.get_for_model(self)
    media_content = property(get_media_content)

    def get_extra_content(self, *args, **kwargs):
        return ExtraContent.objects.get_for_model(self)
    extra_content = property(get_extra_content)

    def parse_content(self):
        parsed_content = None
        try:
            c = self.content_rendered.replace('\r\n\t','')
            parsed_content = json.loads(c)
        except ValueError:
            logger.warning('error parsing')
            pass
        return parsed_content

    def get_first_paragraph(self):
        parsed_content = self.parse_content()

        if not isinstance(parsed_content, collections.Iterable) \
                and isinstance(parsed_content, basestring):
            extract = parsed_content.split('<!--more-->')
            return extract[0]
 
        elif isinstance(parsed_content, collections.Iterable):
            for row in parsed_content:
                for obj in row:
                    if obj['type'] == 'p':
                        return obj

        return ""
    first_paragraph = property(get_first_paragraph)

    def get_images(self):
        return MediaContent.objects.get_for_model(self).filter(mimetype__startswith='image')
    images = property(get_images)

    def get_first_image(self):
        images = self.get_images()
        if images:
            return images[0]

        parsed_content = self.parse_content()
        
        if isinstance(parsed_content, collections.Iterable):
            if parsed_content:
                for row in parsed_content:
                    for obj in row:
                        if obj['type'] == 'img' or obj['type'] == 'video:youtube':
                            return obj

        if not parsed_content or isinstance(parsed_content, basestring):
            import re
            imgtag = re.compile(r'<img[^>]*\ssrc="(.*?)"')
            images = imgtag.findall(self.content_rendered)
            if images:
                logger.info('imagen %s', images[0]) 
                return images[0]

        return ""
    first_image = property(get_first_image)
