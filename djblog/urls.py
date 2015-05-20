# *-* coding:utf-8 *-*
try:
    from django.conf.urls.defaults import patterns, include, url
except ImportError:
    from django.conf.urls import patterns, include, url

from django.conf import settings
from djblog.views.post import *
from djblog.views.page import *

# Custom URLs
urlpatterns = patterns('',
#    url(r?'^(?P<slug>[\w\-\_\./])$', )
)

# Haystack config
if 'haystack' in getattr(settings, 'INSTALLED_APPS', []):
    from djblog.views.search import *

    urlpatterns += patterns('',
        url(r'^buscar/', CustomSearchView(), name="haystack_search"),
    )

# Post (CmsConfig)
#   [post_detail]               /aaaa/mm/dd/slug[_n]/
#   [post_year_list]            /aaaa/
#   [post_year_month_list]      /aaaa/mm/
#   [post_year_month_day_list]  /aaaa/mm/dd/
#   [post_thisweek_list]        /thisweek/
#   [post_today_list]           /today/
#   [post_category_list]        /category/slug/
#   [post_author_list]          /author/slug/
#   [post_tag_list]             /tag/slug/
#   [post_search_list]          /search/?q=QUERY+PARAMS
urlpatterns += patterns('',
    url(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w\-\_\.]+)/?$', PostDateDetailView.as_view(), name='post_detail'), 
    url(r'^post/(?P<year>[0-9]{4})/?$', PostYearListView.as_view(), name='post_year_list'), 
    url(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/?$', PostMonthListView.as_view(), name='post_year_month_list'), 
    url(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', PostDayListView.as_view(), name='post_year_month_day_list'), 
    url(r'^post/thisweek/?$', PostWeekListView.as_view(), name='post_thisweek_list'),
    url(r'^post/today/?$', PostWeekListView.as_view(), name='post_today_list'),
    url(r'^post/category/(?P<slug>[\w\-\_\.]+)/?$', PostCategoryListView.as_view(), name='post_category_list'),
    url(r'^post/author/(?P<slug>[\w\-\_\.]+)/?$', PostAuthorListView.as_view(), name='post_author_list'),
    url(r'^post/tag/(?P<slug>[\w\-\_\.]+)/?$', PostTagListView.as_view(), name='post_tag_list'),
    url(r'^post/?$', PostLatestListView.as_view(), name='post_latest_list'),
    url(r'^(?P<slug>[\w\-\_\.]+)/?$', PostDetailView.as_view(), name='post_canonical_detail'),
)

# Page (CmsConfig)
#   [page_detail]               /slug/
#   [page_hierarchy_detail]     /slug[_parent]/slug/
#   [page_category_list]        /slug/
urlpatterns += patterns('',
    url(r'^page/(?P<slug>[\w\-\_\.]+)/?$', PageDetailView.as_view(), name='page_detail'),
    url(r'^page/category/(?P<slug>[\w\-\_\.]+)/?$', PageCategoryListView.as_view(), name='page_category_list'),
    url(r'^page/(?P<category_slug>[\w\-\_\.]+)/(?P<hierarchy_slug>[\w\-\_\./]+)$', PageHierarchyDetailView.as_view(), name='page_hierarchy_detail'),
)
