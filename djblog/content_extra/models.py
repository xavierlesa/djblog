# *-* coding:utf-8 *-*
"""
Una app para cargar contenidos extra

"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.encoding import force_unicode

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
        qs = self.get_query_set().filter(content_type=ct)

        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs


class ExtraContent(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_pk')
    
    key = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    field = models.TextField()
    #fieldtype = models.CharField(max_length=20, choices=FIELD_TYPE)

    
    objects = ExtraContentManager()

    class Meta:
        app_label = 'djblog'

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

################################################################################
# prueba de install
################################################################################

