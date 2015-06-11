# -*- coding:utf-8 -*-

try:
    from django.conf.urls.defaults import patterns, include, url
except ImportError:
    from django.conf.urls import patterns, include, url

from django.conf import settings
from djblog.views.post import *
from djblog.views.page import *


urlpatterns = patterns('',
        )

# Haystack config
if 'haystack' in getattr(settings, 'INSTALLED_APPS', []):
    from djblog.views.search import *

    urlpatterns += patterns('',
        url(r'^buscar/', CustomSearchView(), name="haystack_search"),
    )

# Post (CmsConfig)
#   [blog_detail]               /aaaa/mm/dd/slug[_n]/
#   [blog_year_list]            /aaaa/
#   [blog_year_month_list]      /aaaa/mm/
#   [blog_year_month_day_list]  /aaaa/mm/dd/
#   [blog_thisweek_list]        /thisweek/
#   [blog_today_list]           /today/
#   [blog_category_list]        /category/slug/
#   [blog_author_list]          /author/slug/
#   [blog_tag_list]             /tag/slug/
#   [blog_search_list]          /search/?q=QUERY+PARAMS
urlpatterns += patterns('',
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w\-\_\.]+)/?$', 
        PostDateDetailView.as_view(), 
        name='blog_detail'), 

    url(r'^blog/(?P<year>[0-9]{4})/?$', 
        PostYearListView.as_view(), 
        name='blog_year_list'), 

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/?$', 
        PostMonthListView.as_view(), 
        name='blog_year_month_list'), 

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', 
        PostDayListView.as_view(), 
        name='blog_year_month_day_list'), 

    url(r'^blog/thisweek/?$', 
        PostWeekListView.as_view(), 
        name='blog_thisweek_list'),

    url(r'^blog/today/?$', 
        PostWeekListView.as_view(), 
        name='blog_today_list'),

    url(r'^blog/category/(?P<slug>[\w\-\_\.]+)/?$',
        PostCategoryListView.as_view(), 
        name='blog_category_list'),

    url(r'^blog/author/(?P<slug>[\w\-\_\.]+)/?$', 
        PostAuthorListView.as_view(), 
        name='blog_author_list'),

    url(r'^blog/tag/(?P<slug>[\w\-\_\.]+)/?$', 
        PostTagListView.as_view(), 
        name='blog_tag_list'),

    url(r'^blog/(?P<slug>[\w\-\_\.]+)/?$', 
        PostDetailView.as_view(), 
        name='blog_canonical_detail'),

    url(r'^blog/?$', 
        PostLatestListView.as_view(), 
        name='blog_latest_list'),
)

# Page (CmsConfig)
#   [page_detail]               /slug/
#   [page_hierarchy_detail]     /slug[_parent]/slug/
#   [page_category_list]        /slug/
urlpatterns += patterns('',
    url(r'^page/(?P<slug>[\w\-\_\.]+)/?$', 
        PageDetailView.as_view(), 
        name='page_detail'),

    url(r'^page/category/(?P<slug>[\w\-\_\.]+)/?$', 
        PageCategoryListView.as_view(), 
        name='page_category_list'),

    url(r'^page/(?P<category_slug>[\w\-\_\.]+)/(?P<hierarchy_slug>[\w\-\_\./]+)$', 
        PageHierarchyDetailView.as_view(), 
        name='page_hierarchy_detail'),

)

# Custom URLs
urlpatterns += patterns('',
    url(r'^(?P<post_type_slug>[\w\-\_\.]+)/(?P<slug>[\w\-\_\.]+)/?$', 
        GenericPostDetailView.as_view(), 
        name='generic_post_detail'),

    url(r'^(?P<post_type_slug>[\w\-\_\.]+)/?$', 
        GenericPostListView.as_view(), 
        name='generic_post_list'),

    url(r'^(?P<post_type_slug>[\w\-\_\.]+)/category/(?P<slug>[\w\-\_\.]+)/?$', 
        GenericCategoryListView.as_view(), 
        name='generic_category_list'),
)


