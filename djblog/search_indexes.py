# -*- coding:utf-8 -*-

import datetime
from haystack import indexes
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djblog.models import Post
import logging
logger = logging.getLogger(__name__)

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    post_type = indexes.CharField()

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Post.objects.active_no_lang()
    
    def read_queryset(self, using=None):
        return self.index_queryset()
    
    def get_model(self):
        return Post

    def prepare_post_type(self, post):
        return post.post_type.slug
