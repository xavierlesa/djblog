# *-* coding=utf-8 *-*

from markdown import markdown
from django.conf.urls.defaults import *
from django.conf import settings
#from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils import translation
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify, striptags, truncatewords, \
        truncatewords_html, force_escape, escape, linebreaksbr, urlize
from nebula.djblog.models import Post, Tag
#from django.template.defaultfilters import markup

SITE = Site.objects.get_current()

# default to 24 hours for feed caching
DJBLOG_FEED_TIMEOUT = getattr(settings, 'DJBLOG_FEED_TIMEOUT', 86400)
DJBLOG_PAGINATION = getattr(settings, 'DJBLOG_PAGINATION', 15)

class LatestFeed(Feed):

    def title(self):
        return "%s Posts" % SITE.name

    def link(self):
        return reverse('post_latest_list')

    def items(self):
        key = 'djblog_feed_latest'
        qs = cache.get(key)
        cur_language = translation.get_language()

        if qs is None:

            qs = list(Post.objects.get_posts().order_by('-publication_date')[:DJBLOG_PAGINATION])
            cache.set(key, qs, DJBLOG_FEED_TIMEOUT)

        return qs

    def item_link(self, obj):
        return obj.get_absolute_url() #reverse('djblog_latest')

    def item_author_name(self, item):
        return item.author.username

    def item_tags(self, item):
        return [c.name for c in item.tags.all()] + [keyword.strip() for keyword in item.keywords.split(',')]

    def item_pubdate(self, item):
        return item.publication_date

#    def get_object(self, request, id):
#        return get_object_or_404(Post.objects.get_posts(), pk=id)
#
#    def item_description(self, item):
#        image = item.first_image
#        image_src = ''
#        if image:
#            if image.content.url:
#                image_src = "<img src='%s' />" % image.content.url
#            else:
#                image_src = "<img src='%s' />" % image.content
#
#        return mark_safe(image_src + markdown(item.first_paragraph['content'], ['extra',]))


class CategoryFeed(Feed):
    pass

class TagFeed(Feed):
    pass

class AuthorFeed(Feed):
    pass


################################################################################
# Nuevo formato ATOM
################################################################################
from django.utils import feedgenerator
from datetime import datetime

class AtomFeedView(Feed):

    feed_type = feedgenerator.RssUserland091Feed #Atom1Feed

    def item_content_encoded(self, item):
        return "<![CDATA[%s]]>" % item.content  

    def title(self):
        return "%s Posts" % SITE.name

    def link(self):
        return reverse('post_latest_list')

    def items(self):
        key = 'djblog_feed_atom'
        qs = cache.get(key)
        cur_language = translation.get_language()

        if qs is None:

            qs = list(Post.objects.get_posts().order_by('-publication_date')[:DJBLOG_PAGINATION])
            cache.set(key, qs, DJBLOG_FEED_TIMEOUT)

        return qs

    def item_link(self, obj):
        return obj.get_absolute_url() #reverse('djblog_latest')

    def item_author_name(self, item):
        return item.author.username

    def item_tags(self, item):
        return [c.name for c in item.tags.all()] + [keyword.strip() for keyword in item.keywords.split(',')]

    def item_pubdate(self, item):
        return item.publication_date

#    def get_object(self, request, *args, **kwargs):
#        print args, kwargs
#        return get_object_or_404(Post.objects.get_posts(), pk=id)

    def item_description(self, item):
        image = item.first_image
        image_src = ''
        if image:
            if image.content.url:
                image_src = "<img src='http://%s%s' />" % (SITE.domain, image.content.url)
            else:
                image_src = "<img src='%s' />" % image.content

        return mark_safe(image_src + markdown(item.first_paragraph['content'], ['extra',]))




################################################################################
# URLs
################################################################################
urlpatterns = patterns('',
    # latest feed
    url('^$', LatestFeed(), name='djblog_feed'),

    # feed by category
    url(r'^category/(?P<category>[a-zA-Z0-9\-\_\.\/]+)$', CategoryFeed(), name='djblog_feed_category'),

    # feed by tag
    url(r'^tag/(?P<tag>[a-zA-Z0-9\-\_\.]+)$', TagFeed(), name='djblog_feed_tag'),

    # feed by author
    url(r'^author/(?P<username>[a-zA-Z0-9\-\_\.]+)$', AuthorFeed(), name='djblog_feed_author'),

    # atom
    url(r'^atom.xml$', AtomFeedView(), name='djblog_feed_atom'),

)


