# *-* coding:utf-8 *-*

from tastypie.resources import ModelResource
from tastypie.authorization import ReadOnlyAuthorization as Authorization # security reasons
from tastypie.serializers import Serializer
from tastypie import fields
from django.core.serializers import json as json_serializer # nebula.djblog.models.* overrides json
from django.utils import simplejson
from nebula.djblog.models import *


class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(
                data, 
                cls=json_serializer.DjangoJSONEncoder,
                sort_keys=True, 
                ensure_ascii=False, 
                indent=self.json_indent
        )


class CategoryResource(ModelResource):
    parent = fields.ForeignKey('self', 'parent', null=True)
    
    class Meta:
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        queryset = Category.objects.active()


class PostCategoryResource(ModelResource):
    parent = fields.ForeignKey('self', 'parent', null=True)
    
    class Meta:
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        queryset = Category.objects.active().filter(blog_category=True)

class PostResource(ModelResource):
    category = fields.ToManyField(PostCategoryResource, 'category', full=True)

    class Meta:
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        queryset = Post.objects.active().filter(is_page=False)


class PageCategoryResource(ModelResource):
    parent = fields.ForeignKey('self', 'parent', null=True)
    
    class Meta:
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        queryset = Category.objects.active().exclude(blog_category=True)

class PageResource(ModelResource):
    category = fields.ToManyField(PageCategoryResource, 'category', full=True)

    class Meta:
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        queryset = Post.objects.active().filter(is_page=True)
