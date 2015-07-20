# -*- coding:utf-8 -*-

from django.conf import settings
import logging
logger = logging.getLogger(__name__)

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from djblog.models import Post

#
# Haystack View
#
class CustomSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        super(CustomSearchView, self).__init__(*args, **kwargs)
        self.searchqueryset = SearchQuerySet().models(Post)
