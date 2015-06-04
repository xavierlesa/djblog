# *-* coding:utf-8 *-*

import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.contrib.sites.models import Site
from django.views.generic import *


"""
ArchiveIndexView, DeleteView, ListView, 
TodayArchiveView, YearArchiveView, CreateView, DetailView, MonthArchiveView, 
UpdateView, DateDetailView, FormView, RedirectView, View, DayArchiveView, 
GenericViewError, TemplateView, WeekArchiveView
"""

from djblog.models import Tag, Status, Category, Post

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

#from nebula.dynaform.views import DynaformMixin
class DynaformMixin:
    pass

class PageBase(DynaformMixin):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = getattr(settings, 'DJBLOG_PAGINATION', 15)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.get_for_lang().filter(post_type__post_type_slug='page')
        return Post.objects.get_pages()

    def get_current_site(self):
        return Site.objects.get_current()

class PageDetailView(PageBase, DetailView):

    def get_template_names(self):
        names = super(PageDetailView, self).get_template_names()
        page_slug = self.kwargs.get('slug', '')

        categories_site_templates = []
        categories_templates =[]

        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        for cat in self.object.category.all():
            categories_site_templates.append('djblog/%s/%s/page_detail.html' % (self.get_current_site().domain, cat.slug))
            categories_templates.append('djblog/%s/page_detail.html' % cat.slug)

        templates.extend(categories_site_templates)
        templates.extend(categories_templates)
        templates.extend((
            'djblog/%s/page_detail.html' % self.get_current_site().domain,
            'djblog/%s_page_detail.html' % page_slug,
            'djblog/%s/%s_page_detail.html' % (self.get_current_site().domain, page_slug),
            'djblog/page_%s.html' % page_slug,
            'djblog/%s/page_%s.html' % (self.get_current_site().domain, page_slug),
            'djblog/page_detail.html',
        ))

        templates.extend(names)

        if self.object.template_name:
            templates.insert(0, self.object.template_name)

        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates


class PageCategoryListView(PageBase, ListView):
    def get_template_names(self):
        names = super(PageCategoryListView, self).get_template_names()
        category_slug = self.kwargs.get('slug', '')

        templates = []
        
        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        r = (
            'djblog/%s/page_list.html' % self.get_current_site().domain,
            'djblog/%s/page_list.html' % category_slug,
            'djblog/%s_page_list.html' % category_slug,
        )

        if hasattr(self, 'category'):
            if self.category.parent:
                r += (
                    'djblog/%s/page_list.html' % self.category.parent.slug,
                )

        r += (
            'djblog/%s/%s/page_list.html' % (self.get_current_site().domain, category_slug),
            'djblog/%s/%s_page_list.html' % (self.get_current_site().domain, category_slug),
            'djblog/page_list.html',
        )

        templates.extend(r)
        templates.extend(names)
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates

    def get_queryset(self, *args, **kwargs):
        category_slug = self.kwargs.get('slug', '')
        queryset = super(PageCategoryListView, self).get_queryset(*args, **kwargs)

        return queryset.filter(Q(category__slug=category_slug)|Q(category__parent__slug=category_slug)).distinct()

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs.get('slug', '')
        context = super(PageCategoryListView, self).get_context_data(**kwargs)
        try:
            self.category = Category.objects.get(slug=category_slug)
            context['category'] = self.category
        except Category.DoesNotExist:
            self.category = None
        return context


class PageHierarchyDetailView(PageBase, DetailView):
    def get_template_names(self):
        names = super(PageHierarchyDetailView, self).get_template_names()
        category_slug = self.kwargs.get('category_slug', '')
        
        templates = []

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)
        
        r = (
            'djblog/%s/page_detail.html' % self.get_current_site().domain,
            'djblog/%s/page_detail.html' % category_slug,
        )

        if hasattr(self, 'category') and self.category.parent:
            r += (
                'djblog/%s/page_detail.html' % self.category.parent.slug,
            )

        r += (
            'djblog/%s_page_detail.html' % category_slug,
            'djblog/%s/%s/page_detail.html' % (self.get_current_site().domain, category_slug),
            'djblog/%s/%s_page_detail.html' % (self.get_current_site().domain, category_slug),
            'djblog/page_detail.html',
        )

        templates.extend(r)
        templates.extend(names)

        if self.object.template_name:
            templates.insert(0, self.object.template_name)

        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()
        hierarchy_slug = self.kwargs.get('hierarchy_slug', '').strip('/')
        slugs = hierarchy_slug.split('/')
        slug = slugs.pop()

        try:
            obj = queryset.get(slug=slug)
        except ObjectDoesNotExist:
            raise Http404()
        
        return obj

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs.get('category_slug', '')
        context = super(PageHierarchyDetailView, self).get_context_data(**kwargs)

        try:
            self.category = Category.objects.get(slug=category_slug)
            context['category'] = self.category
        except Category.DoesNotExist:
            pass
        return context
