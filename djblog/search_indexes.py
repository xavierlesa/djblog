# -*- coding:utf-8 -*-

import datetime
from haystack import indexes
#from haystack import site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djblog.models import Post
import logging
logger = logging.getLogger(__name__)

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    site = indexes.CharField(model_attr='site')
    lang = indexes.CharField(model_attr='lang')
    is_page = indexes.BooleanField(model_attr='is_page')
    category = indexes.CharField(model_attr='category')

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return Post.objects.public().filter(pub_date__lte=datetime.datetime.now())
        return Post.objects.active_no_lang()
    
    def read_queryset(self, using=None):
        return self.index_queryset()
    
    def get_model(self):
        return Post

    def prepare_category(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])

    def prepare_site(self, obj):
        return ", ".join([cat.name for cat in obj.site.all()])

#site.register(Post, PostIndex)
