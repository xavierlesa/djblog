Django Blog
===========

App para crear contenido dinamico, como un blog

## Instalación

```
pip install git+http://github.com/ninjaotoko/djblog
```

Luego agregar entre tus ```INSTALLED_APPS ```:

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'djblog',
    ...
    )
```

Y en tus ```urls.py```

```
urlpatterns = [
    ...
    url(r'^admin/', include(admin.site.urls)),
    ...
    url(r'', include('djblog.urls')),
    ]
```

Ahora haces ```python manage.py migrate``` y listo!


## URLs y Vistas que djblog trae de fábrica

Por defecto djblog trae dos tipos de contenidos, los ```Post``` y las ```Page```
estos objetos tiene una estructura un poco diferente de URLs en comparación con
las genéricas.

### Post URLs ###

|URL name                   |URL formato                          |
|---------------------------|-------------------------------------|
|*blog_detail*              |`/blog/<year>/<month>/<day>/<slug>/ `|
|*blog_year_list*           |`/blog/<year>                       `|
|*blog_year_month_list*     |`/blog/<year>/<month>               `|
|*blog_year_month_day_list* |`/blog/<year>/<month>/<day>/        `|
|*blog_thisweek_list*       |`/blog/thisweek/                    `|
|*blog_today_list*          |`/blog/today/                       `|
|*blog_category_list*       |`/blog/category/<slug>/             `|
|*blog_author_list*         |`/blog/author/<slug>/               `|
|*blog_tag_list*            |`/blog/tag/<slug>/                  `|
|*blog_canonical_detail*    |`/blog/<slug>/                      `|
|*blog_latest_list*         |`/blog/                             `|


### Page URLs ###

|URL name                   |URL formato                              |
|---------------------------|-----------------------------------------|
|*page_detail*              |`/page/<slug>/                          `|
|*page_category_list*       |`/page/category/<slug>/                 `|
|*page_hierarchy_detail*    |`/page/<category_slug>/<hierarchy_slug>/`|
    

### Objetos genéricos y búsqueda ###

|URL name                   |URL formato                         |
|---------------------------|------------------------------------|
|**Search** (haystack)      |                                    |
|*generic_post_detail*      |`/<post_type_slug>/<slug>/         `|
|*generic_post_list*        |`/<post_type_slug>/                `|
|*generic_category_list*    |`/<post_type_slug>/category/<slug>/`|


Sí ```haystack``` está instalado habilita la URL de búsqueda

|URL name                   |URL formato              |
|---------------------------|-------------------------|
|*haystack_search*          |`/buscar/?q=QUERY+PARAMS`|


## Templatetags

### post_title ###
Devuelve el título de un post/pagina

```
{% post_title %}
```

Por defecto ```post_title``` resuelve el ```object``` desde el contexto, pero es posible pasar uno desde los argumentos.

```
{% post_title [object=post [limit=12]] %}
```

Es posible limitar la cantidad de caracteres pasando el argumento limit.


### post_image ###
Devuelve la imagen principal asociada al post/page

```
{% post_image [size=[320x200|thumbnail|gallery] [attrs="class='thumb'" [gallery_only=True [thumbnail_only=True]]]] %}
```

No tiene ningún argumento obligatorio, pero si es posible modificar el tamaño y los atributos del tag.

**size**: ```thumbnail``` y ```gallery``` son valores predefinidos pero sino puede ser seteado con width x height, así ```320x200```.
**attrs**: Son pasados cómo vienen al tag ```<img src=... %(attrs)s/>```
**gallery_only**: Determina si solo usa la imagen tildada como ```gallery_only```
**thumbnail_only**: Determina si solo usa la imagen tildada como ```thumbnail_only```


### post_extract ###
Genera el extracto a partir del contenido.

```
{% post_extract %}
```

Por defecto ```post_extract``` resuelve el ```object``` desde el contexto, pero es posible pasar uno desde los argumentos.

```
{% post_extract object=post [splitter='<!--more-->' [tag_link='<a href="%s">Leer m&aacute;s</a>' [limit=0 [limit_chars=0 [is_markdown=False [is_safe=False]]]]]] %}
```

Busca primero en el copete si no existe pasa al content_rendered y limita por la cantidad de caracteres, o donde encentre el patron del ```splitter```.


### post_date ###
Retorna la fecha el post/page ```publication_date```.

```
{% post_date [format="l j, F"] %}
```

User los siguientes formatos https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date


### post_content ###
Retorna el contenido renderizado del post/page ```content_render```

```
{% post_content %}
```

### post_link ###
Devuelve el un `dict` con la `url` y `attribs` de un objeto o la url absoluta.

Sí tiene `extra_content` asociado con `key`='link' usa éste para generar la URL.
Sí el flag extra_content_only es True, solo devuelve un link si éste está 
asociado a `extra_content`.

key=link,
name:
    url -> href
    attribs -> atributos del tag A

```
{% post_link [extra_content_only=False] %}
```

### post_archive ###
Retorna un ```QuerySet``` con el "Archivo" de los post/page por meses.

```
<ul>
{% post_archive as archive_list %}
{% for archive in archive_list %}
<li><a href="{{ archive.get_absolute_url }}">{{ archive }}</a></li>
{% endfor %}
</ul>
```


### get_pages_from_category ###
Devuelve el ```QuerySet``` de ```page``` para una categoría.

```
{% get_pages_from_category cat='category-slug' [recursive=recursive] as object_list %}
```

Si se quiere incluir las categorías ```childs``` hay que agregar el argumento ```recursive=recursive```


### get_posts_from_category ###
Devuelve el ```QuerySet``` de ```post``` para una categoría.

```
{% get_posts_from_category cat='category-slug' [recursive=recursive] as object_list %}
```

Si se quiere incluir las categorías ```childs``` hay que agregar el argumento ```recursive=recursive```


### get_post_or_page ###
Retorna un ```post``` o ```page``` por ```slug``` o ```ID```

```
{% get_post_or_page [id=23|slug=acerca-de] as object %}
```

> Nuevo en v 0.2

### get_posts_from_post_type ###
Retorna un QuerySet filtrando el `post_type` del argumento o el mismo post_type del `contexto['object']`

```
{% get_posts_from_post_type [post_type='post_type_slug'|post_type=<post_type_instance>] as object_list %}
```

### get_category ###
Retorna una ```category``` por ```slug```

```
{% get_category slug='category-name' as object %}
```

### get_all_categories ###

```
{% get_all_categories [slug=category-name blog=False children=False recursive=False max_level=2] as object_list %}
```

Retorna el `QueySet` de Category según algunos filtros.
Si el `slug` está presente filtra por aquellas `Category` que tengan como
parent este `slug`.

Si el `slug` y `children` es `True` también filtra por aquellas que también
tengan este `slug`, es decir filtra por aquellas que tengan el `slug` como 
child o parent.

El argumento `blog` filtra el `QueySet` por `Category` de `blog`, con el 
flag `blog_category=True`.

`recursive` busca de forma recursiva la conincidencia del `slug` con un máximo
de 2 niveles por defecto, pero se puede ajustar desde `max_level`.


### get_sub_categories ###
Retorna las ```category``` del post/page donde el ```parent``` es el ```slug``` del argumento.

```
{% get_sub_categories slug=category-name as object_list %}
```

### get_posts_for_tags ###
Filtra por `taxonomia` los `post` con los `tags` asociados

```
{% get_posts_for_tags [tags='perro,gato,liebre'] [id='1,34,56'] [<Tag: object>] [<Tag QuerySet>] as object_list %}
```


### get_tags_list ###
Retorna todos los `tags` acumulados

```
{% get_tags_list as object_list %}
```


## Filtros 

### post_video ###

> Warning: Este filtro está deprecated hay que usar post_embed y usar tagembed para
> resolver los embeds

Devuelve un video asociado, busca en ```extra_content``` si tiene un objeto con el ```key``` ```video```.
En caso de no tener busca en las columnas del ```parse_content``` con el tipo ```video:youtube```

```
{{ object|post_video }}
```

### get_post_extra_content_key_name ###
Devuelve los ```extra_content``` asociados al post/page filtrando por ```key``` y ```name```

```
{{ object|get_post_extra_content_key_name:'pdf:attached' }}
```


## get_post_extra_content_key 
Devuelve los ```extra_content``` asociados al post/page filtrando por ```key```

```
{{ object|get_post_extra_content_key:'pdf' }}
```


### get_post_extra_content_by_keys ###
Devuelve los ```extra_content``` asociados al post/page filtrando por mas de una ```key```

```
{{ object|get_post_extra_content_by_keys:'pdf,doc,txt' }}
```


### extract ###
Devuelve el contenido del post/page partido por el ```splitter```

```
{{ object|extract:'<!--more-->' }}
```


### has_category ###
Retorna ```True``` si la categoría está asociada al post/page

```
{{ object|has_category:'slug-of-category' }}
```

> Nuevo en v0.2
### exclude_object ###
Excluye un `object` desde el `QuerySet` por su `ID`

```
{{ object_list|exclude_object:object }}
```
