Django Blog
===========

App para crear contenido dinamico, como un blog


# Templatetags

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


## get_posts_from_category 
Devuelve el ```QuerySet``` de ```post``` para una categoría.

```
{% get_posts_from_category cat='category-slug' [recursive=recursive] as object_list %}
```

Si se quiere incluir las categorías ```childs``` hay que agregar el argumento ```recursive=recursive```


## get_post_or_page 
Retorna un ```post``` o ```page``` por ```slug``` o ```ID```

```
{% get_post_or_page [id=23|slug=acerca-de] as object %}
```


## get_category 
Retorna una ```category``` por ```slug```

```
{% get_category slug='category-name' as object %}
```

## get_all_categories 

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


## get_sub_categories 
Retorna las ```category``` del post/page donde el ```parent``` es el ```slug``` del argumento.

```
{% get_sub_categories slug=category-name as object_list %}
```

## get_posts_for_tags 
Filtra por `taxonomia` los `post` con los `tags` asociados

```
{% get_posts_for_tags [tags='perro,gato,liebre'] [id='1,34,56'] [<Tag: object>] [<Tag QuerySet>] as object_list %}
```


## get_tags_list 
Retorna todos los `tags` acumulados

```
{% get_tags_list as object_list %}
```


# Filtros 

## post_video 
Devuelve un video asociado, busca en ```extra_content``` si tiene un objeto con el ```key``` ```video```.
En caso de no tener busca en las columnas del ```parse_content``` con el tipo ```video:youtube```

```
{{ object|post_video }}
```

## get_post_extra_content_key_name 
Devuelve los ```extra_content``` asociados al post/page filtrando por ```key``` y ```name```

```
{{ object|get_post_extra_content_key_name:'pdf:attached' }}
```


## get_post_extra_content_key 
Devuelve los ```extra_content``` asociados al post/page filtrando por ```key```

```
{{ object|get_post_extra_content_key:'pdf' }}
```


## get_post_extra_content_by_keys 
Devuelve los ```extra_content``` asociados al post/page filtrando por mas de una ```key```

```
{{ object|get_post_extra_content_by_keys:'pdf,doc,txt' }}
```


## extract 
Devuelve el contenido del post/page partido por el ```splitter```

```
{{ object|extract:'<!--more-->' }}
```


## has_category 
Retorna ```True``` si la categoría está asociada al post/page

```
{{ object|has_category:'slug-of-category' }}
```
