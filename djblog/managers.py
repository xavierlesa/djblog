# *-* coding:utf-8 *-*

from django.db import models
from django.utils.timezone import now as tz_now
from django.conf import settings
from django.utils.decorators import wraps
from logging import debug as __
from djblog.common.managers import MultiSiteBaseManager

NEBULA_FLAGS = getattr(settings, 'NEBULA_FLAGS', {})

class SiteBlogManager(MultiSiteBaseManager):
    """
    live: son aquellos objetos que no se han borrado, es solo útil si no se quieren borrar permanentemente.
    active: son los objetos que puede ser visibles en el front.
    """
    def live(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(is_live=True)

    def active(self, *args, **kwargs):
        return self.live(*args, **kwargs).filter(is_active=True)



class BaseManager(MultiSiteBaseManager):
    """
    live: son aquellos objetos que no se han borrado, es solo útil si no se quieren borrar permanentemente.
    active: son los objetos que puede ser visibles en el front.
    """
    def live_no_lang(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(is_live=True)

    def live(self, *args, **kwargs):
        return self.get_for_lang(*args, **kwargs).filter(is_live=True)

    def active_no_lang(self, *args, **kwargs):
        return self.live_no_lang(*args, **kwargs).filter(is_active=True)

    def active(self, *args, **kwargs):
        return self.live(*args, **kwargs).filter(is_active=True)



class TagManager(BaseManager):
    def for_site(self, *args, **kwargs):
        return self.active(*args, **kwargs)


class CategoryManager(BaseManager):
    """
    blog: es para que solo muestre aquells categorías que son de blog, y no las de páginas.
    page: para que traiga las categorías de páginas.
    """
    
    def active(self, *args, **kwargs):
        qs = super(CategoryManager, self).active(*args, **kwargs)

        if NEBULA_FLAGS.get('BLOG_CATEGORY_SHOW_LIST', False):
            qs = qs.filter(show_on_list=True)

        return qs

    def blog(self, *args, **kwargs):
        return self.active(*args, **kwargs).filter(blog_category=True)

    def noblog(self, *args, **kwargs):
        return self.active(*args, **kwargs).exclude(blog_category=True) # puede ser None o False



class PostManager(BaseManager):

    def public(self, *args, **kwargs):
        """
        obtiene todo lo que este activo, no expiro y ya fue publicado
        """

        now = tz_now()
        qs = self.active(*args, **kwargs)
        return qs.filter(models.Q(expiration_date__gte=now) | models.Q(expiration_date__isnull=True), 
                publication_date__lte=now,
                status__is_public=True)


    def get_posts(self, *args, **kwargs):
        """
        obtiene los posts publicados
        """
        qs = self.public(*args, **kwargs)
        return qs.filter(post_type__post_type_slug='blog')

    def get_pages(self, *args, **kwargs):
        """
        obtiene las paginas publicadas
        """
        qs = self.public(*args, **kwargs)
        return qs.filter(post_type__post_type_slug='page')

    def get_blog_posts(self, *args, **kwargs):
        """
        obtiene todo lo que sea un post y este publicado
        """
        qs = self.get_posts(*args, **kwargs)
        # DEPRECATED
        #return qs.filter(models.Q(category__blog_category=True) | models.Q(category__isnull=True)).distinct() # no mostrar repetidos
        return qs
        

    def get_noblog_posts(self, *args, **kwargs):
        """
        obtiene todo lo que sea un post noblog y este publicado
        """
        qs = self.get_posts(*args, **kwargs)
        # DEPRECATED
        #return qs.exclude(models.Q(category__blog_category=True) | models.Q(category__isnull=True)).distinct() # no mostrar repetidos
        return qs

    def get_generic_posts(self, *args, **kwargs):
        """
        filtra el blog y las páginas para devolver los objetos genéricos
        """
        EXCLUDED_SLUGS = ['blog', 'page']
        post_type = kwargs.pop("post_type", None)

        if post_type:
            if post_type.post_type_slug in EXCLUDED_SLUGS:
                EXCLUDED_SLUGS.remove(post_type.post_type_slug)
        
        qs = self.public(*args, **kwargs).exclude(post_type__post_type_slug__in=EXCLUDED_SLUGS)
        if post_type:
            qs = qs.filter(post_type=post_type)

        return qs
