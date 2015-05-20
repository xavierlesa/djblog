# *-* coding=utf-8 *-*

"""
Nebula es un grupo de aplicaciones desarrolladas para funcionar en conjunto
pero también de forma independiente. Ideada para usarse como Blog, CMS, Portal
o Red Social y/u otro fin que se le quiera dar, no hace cafe :(

Author: Xavier Lesa <xavierlesa@gmail.com>
"""

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.contrib.sites.models import Site
from django.utils import translation
import logging
logger = logging.getLogger(__name__)

__ALL__ = ('MultiSiteBaseManager','MultiSiteBaseManagerAdmin','BaseManager','GenericRelationManager')

class MultiSiteBaseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        """
        Registros para el site actual o sin site 
        """
        qs = super(MultiSiteBaseManager, self).get_queryset(*args, **kwargs)
        qs = qs.filter(models.Q(site__id__in=[Site.objects.get_current().pk,]) | models.Q(site__isnull=True))
        return qs

    def get_for_lang(self, *args, **kwargs):
        """
        Registros para el idioma actual o sin idioma
        """
        qs = self.get_queryset(*args, **kwargs)
        if 'django.middleware.locale.LocaleMiddleware' in getattr(settings, 'MIDDLEWARE_CLASSES', []):
            return qs.filter(models.Q(lang__iexact=translation.get_language()) | models.Q(lang__exact=''))
        else:
            logger.warning('NO get for lang %s', translation.get_language())
        return qs

    def get_for_site_or_none(self, *args, **kwargs):
        """
        Registros para el site actual 
        """
        qs = super(MultiSiteBaseManager, self).get_queryset(*args, **kwargs)
        return qs.filter(site__id__in=[Site.objects.get_current().pk,])


class MultiSiteBaseManagerAdmin(models.Manager):
    pass
    #def get_queryset(self, *args, **kwargs):
    #    """ todos los registros de todos los sites """
    #    return super(MultiSiteBaseManagerAdmin, self).get_queryset(*args, **kwargs)
 

class BaseManager(models.Manager):
    def live(self, *args, **kwargs):
        """
        Solo regsitros vivos 
        """
        return self.get_queryset().filter(is_live=True)

    def active(self, *args, **kwargs):
        """
        Solo registros vivos y activos 
        """
        return self.live().filter(is_active=True)

    def latest_update(self, *args, **kwargs):
        """
        Los últimos editados 
        """
        return self.get_queryset().order_by('-up_date')


class GenericRelationManager(models.Manager):
    def for_model(self, model):
        """
        Para el modelo en particular y/o su instancia o clase 
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs
