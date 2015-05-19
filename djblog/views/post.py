# *-* coding:utf-8 *-*

import datetime
from django.conf import settings
from django.db.models import Q
from django.contrib.sites.models import Site
from django.views.generic import *
from django.contrib.auth.models import User

from nebula.dynaform.views import DynaformMixin
"""
ArchiveIndexView, DeleteView, ListView, 
TodayArchiveView, YearArchiveView, CreateView, DetailView, MonthArchiveView, 
UpdateView, DateDetailView, FormView, RedirectView, View, DayArchiveView, 
GenericViewError, TemplateView, WeekArchiveView
"""

from ..models import Tag, Status, Category, Post

import logging
# Get an instance of a logger
logger = logging.getLogger('nebula')

class PostBase(DynaformMixin):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = getattr(settings, 'DJBLOG_PAGINATION', 15)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.get_for_lang().filter(is_page=False)
        return Post.objects.get_posts()

    def get_current_site(self):
        return Site.objects.get_current()


class PostDateBase(PostBase):
    date_field = 'publication_date'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    week_format = '%W'


class PostLatestListView(PostBase, ListView):
    """
    Lista los últimos posts cargados
    """
    def get_template_names(self):
        names = super(PostLatestListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/latest_post_list.html' % self.get_current_site().domain,
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/latest_post_list.html',
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates


class PostDateDetailView(PostDateBase, DateDetailView):
    """
    Detalle para un post /aaaa/mm/dd/slug-del-post
    """
    def get_template_names(self):
        names = super(PostDateDetailView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_detail.html' % self.get_current_site().domain,
            'djblog/post_detail.html',
        ))

        templates.extend(names)
        return templates


class PostYearListView(PostDateBase, YearArchiveView):
    """
    Lista para posts /aaaa/
    """
    def get_template_names(self):
        names = super(PostYearListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates


class PostMonthListView(PostDateBase, MonthArchiveView):
    """
    Lista para posts /aaaa/mm/
    """
    def get_template_names(self):
        names = super(PostMonthListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates


class PostDayListView(PostDateBase, DayArchiveView):
    """
    Lista para posts /aaaa/mm/dd/
    """
    def get_template_names(self):
        names = super(PostDayListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates


class PostWeekListView(PostDateBase, WeekArchiveView):
    """
    Lista para posts /aaaa/
    """
    def get_template_names(self):
        names = super(PostWeekListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates

    def get_week(self):
        year, week, day_of_week = datetime.datetime.now().isocalendar()
        return week


class PostTodayListView(PostDateBase, TodayArchiveView):
    """
    Lista para posts con fecha de hoy
    """
    def get_template_names(self):
        names = super(PostTodayListView, self).get_template_names()
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/post_list.html',
            'djblog/%s/today_post_list.html' % self.get_current_site().domain,
            'djblog/today_post_list.html',
        ))
    
        templates.extend(names)
        return templates


class PostCategoryListView(PostBase, ListView):
    """
    Lista para posts de una categoria
    """
    def get_template_names(self):
        names = super(PostCategoryListView, self).get_template_names()
        category_slug = self.kwargs.get('slug', '')
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/%s/post_list.html' % (self.get_current_site().domain, category_slug), 
            'djblog/%s/%s_post_list.html' % (self.get_current_site().domain, category_slug),
            'djblog/%s/category_post_list.html' % (self.get_current_site().domain), 
            'djblog/%s/post_list.html' % self.get_current_site().domain, 
            'djblog/%s/post_list.html' % category_slug,
            'djblog/%s_post_list.html' % category_slug,
            'djblog/category_post_list.html',
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates

    def get_queryset(self, *args, **kwargs):
        category_slug = self.kwargs.get('slug', '')
        queryset = super(PostCategoryListView, self).get_queryset(*args, **kwargs).distinct()

        return queryset.filter(Q(category__slug=category_slug)|Q(category__parent__slug=category_slug))

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs.get('slug', '')
        context = super(PostCategoryListView, self).get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=category_slug)
        except (Category.DoesNotExist, Category.MultipleObjectsReturned):
            pass
        return context


class PostAuthorListView(PostBase, ListView):
    """
    Lista para posts de un autor
    """
    def get_template_names(self):
        names = super(PostAuthorListView, self).get_template_names()
        username = self.kwargs.get('slug', '')
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)
        
        templates.extend((
            'djblog/%s/%s/post_list.html' % (self.get_current_site().domain, username),
            'djblog/%s/%s_post_list.html' % (self.get_current_site().domain, username),
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/%s/author_post_list.html' % self.get_current_site().domain,
            'djblog/%s/post_list.html' % username,
            'djblog/%s_post_list.html' % username,
            'djblog/author_post_list.html',
            'djblog/post_list.html',
        ))
        
        templates.extend(names)
        return templates

    def get_queryset(self, *args, **kwargs):
        author_slug = self.kwargs.get('slug', '')
        queryset = super(PostAuthorListView, self).get_queryset(*args, **kwargs).distinct()
        return queryset.filter(author__slug__iexact = author_slug)

    def get_context_data(self, **kwargs):
        """
        Agrega en el `context` el `author` del filtro
        """
        username = self.kwargs.get('slug', '')
        context = super(PostAuthorListView, self).get_context_data(**kwargs)
        try:
            context['author'] = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass
        return context


class PostTagListView(PostBase, ListView):
    """
    Lista los `post` asociados a un `tag`
    """
    def get_template_names(self):
        names = super(PostTagListView, self).get_template_names()
        username = self.kwargs.get('slug', '')
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend((
            'djblog/%s/post_list.html' % self.get_current_site().domain,
            'djblog/%s/tag_post_list.html' % self.get_current_site().domain,
            'djblog/tag_post_list.html',
            'djblog/post_list.html',
        ))

        templates.extend(names)
        return templates

    def get_queryset(self, *args, **kwargs):
        tag_slug = self.kwargs.get('slug', '')
        queryset = super(PostTagListView, self).get_queryset(*args, **kwargs).distinct()
        return queryset.filter(tags__slug__in = [tag_slug])

    def get_context_data(self, **kwargs):
        """
        Agrega al `context` el `tag` del filtro
        """
        tag_slug = self.kwargs.get('slug', '')
        context = super(PostTagListView, self).get_context_data(**kwargs)
        try:
            context['tag'] = Tag.objects.get(slug=tag_slug)
        except (Tag.DoesNotExist, Tag.MultipleObjectsReturned):
            pass
        return context


class PostDetailView(PostBase, DetailView):
    """
    Detalle para un post /slug-del-post
    """

    def get_template_names(self):
        names = super(PostDetailView, self).get_template_names()
        page_slug = self.kwargs.get('slug', '')

        categories_site_templates = []
        categories_templates =[]

        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        for cat in self.object.category.all():
            categories_site_templates.append('djblog/%s/%s/post_detail.html' % (self.get_current_site().domain, cat.slug))
            categories_templates.append('djblog/%s/post_detail.html' % cat.slug)

        templates.extend(categories_site_templates)
        templates.extend(categories_templates)
        templates.extend((
            'djblog/%s/post_detail.html' % self.get_current_site().domain,
            'djblog/%s_post_detail.html' % page_slug,
            'djblog/%s/%s_post_detail.html' % (self.get_current_site().domain, page_slug),
            'djblog/post_%s.html' % page_slug,
            'djblog/%s/post_%s.html' % (self.get_current_site().domain, page_slug),
            'djblog/post_detail.html',
        ))
       
        templates.extend(names)
        logger.debug('Loading theses templates names %s' % templates)
        return templates


#
# Haystack View
#

if 'haystack' in getattr(settings, 'INSTALLED_APPS', []):
    from haystack.views import SearchView
    from haystack.query import SearchQuerySet

    class CustomSearchView(SearchView):
        def __init__(self, *args, **kwargs):
            super(CustomSearchView, self).__init__(*args, **kwargs)
            self.searchqueryset = SearchQuerySet().models(Post).filter(is_page=0)
