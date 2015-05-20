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
        return self.get_query_set(*args, **kwargs).filter(is_live=True)

    def active(self, *args, **kwargs):
        return self.live(*args, **kwargs).filter(is_active=True)



class BlogManager(MultiSiteBaseManager):
    """
    live: son aquellos objetos que no se han borrado, es solo útil si no se quieren borrar permanentemente.
    active: son los objetos que puede ser visibles en el front.
    """
    def live_no_lang(self, *args, **kwargs):
        return self.get_query_set(*args, **kwargs).filter(is_live=True)

    def live(self, *args, **kwargs):
        return self.get_for_lang(*args, **kwargs).filter(is_live=True)

    def active_no_lang(self, *args, **kwargs):
        return self.live_no_lang(*args, **kwargs).filter(is_active=True)

    def active(self, *args, **kwargs):
        return self.live(*args, **kwargs).filter(is_active=True)



class TagManager(BlogManager):
    def for_site(self, *args, **kwargs):
        return self.active(*args, **kwargs)


class CategoryManager(BlogManager):
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



class PostManager(BlogManager):

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
        return qs.exclude(is_page=True)

    def get_pages(self, *args, **kwargs):
        """
        obtiene las paginas publicadas
        """
        qs = self.public(*args, **kwargs)
        return qs.filter(is_page=True)

    def get_blog_posts(self, *args, **kwargs):
        """
        obtiene todo lo que sea un post y este publicado
        """
        qs = self.get_posts(*args, **kwargs)
        return qs.filter(models.Q(category__blog_category=True) | models.Q(category__isnull=True)).distinct() # no mostrar repetidos

    def get_noblog_posts(self, *args, **kwargs):
        """
        obtiene todo lo que sea un post noblog y este publicado
        """
        qs = self.get_posts(*args, **kwargs)
        return qs.exclude(models.Q(category__blog_category=True) | models.Q(category__isnull=True)).distinct() # no mostrar repetidos
