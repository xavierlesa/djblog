# *-* coding:utf-8 *-*
"""
Una app para cargar contenidos extra

"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import force_unicode
from django.template.defaultfilters import striptags

try:
    import json
except ImportError:
    from django.utils import simplejson as json


FIELD_TYPE = (
    ('video', u'Video'),
    ('image', u'Imagen'),
)

class ExtraContentManager(models.Manager):
    def get_for_model(self, model):
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)

        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs

class ExtraContent(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_pk')
    
    key = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    text_field = models.TextField()
    rich_field = models.BooleanField(default=False, blank=True, 
            help_text=_(u"Este estado determina si se mostrara como texto enriquecido o plano"))
    sort_order = models.PositiveIntegerField(_(u'Orden'),default=1) 
    
    objects = ExtraContentManager()

    class Meta:
        app_label = 'djblog'
        ordering = ('sort_order',)


    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        super(ExtraContent, self).save(args, kwargs)

    @property
    def field_json(self):
        try:
            f = json.loads(self.field)
        except:
            f= self.field
        return f

    class API:
        exclude = ('object_pk', 'content_type', 'content_object')

    @property
    def field(self):
        if self.rich_field:
            return self.text_field
        return striptags(self.text_field)
