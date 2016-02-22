# *-* coding=utf-8 *-*

"""
Este es un grupo de aplicaciones desarrolladas para funcionar en conjunto
pero también de forma independiente. Ideada para usarse como Blog, CMS, Portal
o Red Social y/u otro fin que se le quiera dar, no hace cafe :(

Author: Xavier Lesa <xavierlesa@gmail.com>
"""

import re
import django

from datetime import datetime
from django.conf import settings
from django.db import models, IntegrityError
from django.db.models.signals import m2m_changed
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify, striptags, linebreaksbr, \
        urlize, truncatewords, truncatewords_html, force_escape, escape, \
        urlizetrunc
from django.utils.safestring import mark_safe
from djblog.common.managers import *

CONTENT_PREVIEW_WORDS = getattr(settings, 'CONTENT_PREVIEW_WORDS', 40)

__ALL__ = ('MultiSiteBaseModel', 'BaseModel', 'ContentModel', 'CategoryModel', \
        'GenericRelationModel', CONTENT_PREVIEW_WORDS)

if 'django.core.context_processors.i18n' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
    # check django version and add the TEMPLATE_CONTEXT_PROCESSORS in the correct data type
    if django.get_version() < '1.9':
        settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ('django.core.context_processors.i18n', 'djblog.context_processors.site')
    else:
        settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ['django.core.context_processors.i18n', 'djblog.context_processors.site']

if getattr(settings, 'TEMPLATES', False) and len(settings.TEMPLATES): # Django 1.8
    if 'django.template.context_processors.i18n' not in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
        settings.TEMPLATES[0]['OPTIONS']['context_processors'] = settings.TEMPLATES[0]['OPTIONS']['context_processors'] + ['django.template.context_processors.i18n',]

if 'djblog.context_processors.site' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
    settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ('djblog.context_processors.site',)
if getattr(settings, 'TEMPLATES', False) and len(settings.TEMPLATES): # Django 1.8
    if 'djblog.context_processors.site' not in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
        settings.TEMPLATES[0]['OPTIONS']['context_processors'] = settings.TEMPLATES[0]['OPTIONS']['context_processors'] + ['djblog.context_processors.site',]

class MultiSiteBaseModel(models.Model):
    """
    Base para Multi Site y Lang
    """
    lang = models.CharField(max_length=20, blank=True, choices=settings.LANGUAGES) 
    site = models.ManyToManyField(Site, blank=True, null=True, related_name="%(app_label)s_%(class)s_related")

    # el primero es el que luego es llamado con _default_manager
    objects_for_admin = MultiSiteBaseManagerAdmin()
    objects = MultiSiteBaseManager()

    class Meta:
        abstract = True


## simula unique_together para multisitio
#def check_unique_together_with(sender, **kwargs):
#    model_instance = kwargs.get('instance', None)
#    unique_together = getattr(model_instance, 'multisite_unique_together', ())
#    action = kwargs.get('action', None)
#    sites = kwargs.get('pk_set', None)
#    model_rel = kwargs.get('model', None)
#    reverse = kwargs.get('reverse', None)
#
#    if action == 'pre_add' and (isinstance(model_rel, Site) or model_rel is Site):
#        filter_keys = dict(site__id__in=sites, lang=model_instance.lang)
#
#        for f in unique_together:
#            filter_keys.update({f:getattr(model_instance, f)})
#
#        try:
#            exist = model_instance.__class__.objects_for_admin.get(**filter_keys)
#            m = "Existe una instancia %s con estos (key) (val) para estos site(s) %s" % (model_instance.__class__, filter_keys)
#            raise IntegrityError(m)
#        except model_instance.DoesNotExist:
#            pass
#m2m_changed.connect(check_unique_together_with, sender=MultiSiteBaseModel.site.through)


class BaseModel(MultiSiteBaseModel):
    """
    BaseModel esta pensado para objectos que requieren (aunque opcionales) del uso de los meta_keywords y meta_description.
    También ofrece una base para uso de multi-lenguajes, multi-sitios, auto slug, fecha de publicación y los campos de 
    -invisibilidad- y activo/inactivo, éste definitivamente es un buen cominezo para los futuros modelos.
    """
    pub_date = models.DateTimeField(blank=True, verbose_name=_(u"Fecha de creación"))
    up_date = models.DateTimeField(auto_now=True, verbose_name=_(u"Fecha de actualización"))

    slug = models.SlugField(max_length=250)
    
    is_active = models.BooleanField(default=True, verbose_name=_(u"Es activo"), help_text=_(u"activa para usar en el frontend"))
    is_live = models.BooleanField(default=True, verbose_name=_(u"Es visible"), help_text=_(u"NO activo lo hace -invisible-")) 
       
    meta_keywords = models.TextField(blank=True, help_text=_(u"opcional, para el SEO"))
    meta_description = models.TextField(blank=True, help_text=_(u"opcional, para el SEO"))

    objects = BaseManager()
    multisite_unique_together = ('slug',)

    class Meta:
        abstract = True
        ordering = ('-pub_date', '-up_date')

    def __unicode__(self):
        if hasattr(self, 'name'):
            u = self.name
        elif hasattr(self, 'title'):
            u = self.title
        else:
            u = u"%s-%s-%s" % (self._meta.app_label, self._meta.object_name.lower(), self.pub_date)
        return u"%s" % u

    @models.permalink
    def get_absolute_url(self):
        """
        Genera la URLs a travez de decorador @permalink. 
        ej: deberia existir una url con nombre 'djblog_posts'
        """
        return (u'%s_%s' % (self._meta.app_label, self._meta.object_name.lower()), (self.pk, self.slug,))
    
    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = datetime.now()

        #usa la funcion create_new_slug para evitar duplicacion a la hora de corregir el slug
        if not self.slug:
            self.slug = self.create_new_slug()

        return super(BaseModel, self).save(*args, **kwargs)

    def create_new_slug(self):
        """
        Crea un nuevo slug único para el modelo, incrementando un alias si es necesario.
        ej: el-avion-de-papel, el-avion-de-papel-1, el-avion-de-papel-2, ... el-avion-de-papel-n
        """

        if hasattr(self, 'get_slug'):
            slug = self.get_slug()
        elif hasattr(self, 'title'):
            slug = slugify(self.title)
        elif hasattr(self, 'name'):
            slug = slugify(self.name)
        else:
            slug = slugify(u"%s-%s-%s" % (self._meta.app_label, self._meta.object_name.lower(), self.pub_date))

        meta_object = None
        rx = r'^%s(\-[\d]+)?$' % slug #regex para saber si existe el slug
        rx2 = r'^%s\-([\d]+)$' % slug #regex para obtener el numeral
        
        #busca si hay un object con el slug modificado comparando las regex
        try:
            meta_object = self.__class__.objects.filter(slug__regex=rx).exclude(id=self.id).order_by('-slug')[0]
        except:
            pass
        
        while meta_object:
            try:
                i = int(re.findall(rx2, meta_object.slug)[0]) + 1 #intenta obtener el numeral y sumarle 1
            except:
                i = 1 #si no existe, settearlo a 1
            new_slug = u"%s-%s" % (slug,i)
            try:
                meta_object = self.__class__.objects.get(slug=new_slug)
            except:
                slug = new_slug
                break

        return slug

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)


class ContentModel(models.Model):
    """
    Modelo para contenidos. Este modelo esta pensado para carga de contenidos, como árticulos, posts, páginas
    comentarios (con títulos), preguntas/prespuestas y todo lo que incluya un título y una descripción.
    """
    title = models.CharField(max_length=200, verbose_name=_(u"Título"))
    copete = models.TextField(verbose_name=_(u"Copete"), help_text=_(u"Es opcional, y si exsite se usa para el extracto"), blank=True)
    content = models.TextField(verbose_name=_(u"Contenido en texto plano"))
    content_rendered = models.TextField(verbose_name=_(u"Contenido HTML"), help_text=_(u"Este es el contenido a mostrarse, permite marcado"))

    objects = BaseManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.title

    @property
    def preview_content(self):
        return truncatewords(urlizetrunc(self.content, 30), CONTENT_PREVIEW_WORDS)

    @property
    def preview_content_rendered(self):
        return mark_safe(truncatewords_html(urlizetrunc(self.content_rendered, 30), CONTENT_PREVIEW_WORDS))


class CategoryModel(models.Model):
    name = models.CharField(max_length=140, verbose_name=_(u"Título"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    # identifica en que nivel de categoria se encuentra, 0 para root
    level = models.PositiveSmallIntegerField(default=0)

    objects = BaseManager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, 'create_new_slug'):
                self.slug = self.create_new_slug()
            else:
                self.slug = slugify(self.name)

        if self.parent:
            self.level = self.parent.level + 1
        return super(CategoryModel, self).save(*args, **kwargs)

    def get_hierarchy(self):
        return self.level

    def get_children(self):
        return self.children.all()
    
    def get_parents_slugs(self, buf = None):
        if not buf:
            buf =  []
        if self.parent:
            buf.append(self.parent.slug)
            return self.parent.get_parents_slugs(buf)
        return buf[::-1]
        
    def get_path(self, buf = None):
        if not buf:
            buf =  []
        buf.append(self)
        if self.parent:
            return self.parent.get_path(buf)
        return buf[::-1]
        
    def create_child(self, **kwargs):
        c = CategoryModel(**kwargs)
        c.parent = self
        c.save()
    
    def __unicode__(self):
        s = ''
        for x in self.get_path():
            s = '%s / %s' % (s, x.name)
        return s
    
    class Meta:
        abstract = True


class GenericRelationModel(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_pk = models.PositiveIntegerField(_('object PK'), blank=True, null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    objects = GenericRelationManager()

    def __unicode__(self):
        return u"%s" % self.content_object

    class Meta:
        abstract = True


class CustomTemplate(models.Model):
    template_name = models.CharField(max_length=200, blank=True, null=True, 
            help_text=_(u"Define un template para este objeto (post o página). \
                    path/al/template/nombre_template.html"))

    custom_template = models.TextField(verbose_name=_(u"Template HTML/Daango"), 
            blank=True, null=True)

    class Meta:
        abstract = True


    def get_template(self):
        """
        Resuelve el template a utilizar para el render

        """
        
        # Render con template propio
        if self.custom_template:
            return self.custom_template

        # Render con otro template_name
        elif self.template_name:
            return self.template_name

        return None
