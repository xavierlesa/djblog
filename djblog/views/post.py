# *-* coding:utf-8 *-*

import datetime
from django.conf import settings
from django.db.models import Q
from django.contrib.sites.models import Site
from django.views.generic import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

"""
ArchiveIndexView, DeleteView, ListView, 
TodayArchiveView, YearArchiveView, CreateView, DetailView, MonthArchiveView, 
UpdateView, DateDetailView, FormView, RedirectView, View, DayArchiveView, 
GenericViewError, TemplateView, WeekArchiveView
"""

from djblog.models import Tag, Status, Category, Post, PostType

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

#from nebula.dynaform.views import DynaformMixin
class DynaformMixin:
    pass

class PostBase(DynaformMixin):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = getattr(settings, 'DJBLOG_PAGINATION', 15)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.get_for_lang().filter(post_type__post_type_slug='blog')
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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

        if self.object.template_name:
            templates.insert(0, self.object.template_name)

        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
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
        post_slug = self.kwargs.get('slug', '')

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
            'djblog/%s_post_detail.html' % post_slug,
            'djblog/%s/%s_post_detail.html' % (self.get_current_site().domain, post_slug),
            'djblog/post_%s.html' % post_slug,
            'djblog/%s/post_%s.html' % (self.get_current_site().domain, post_slug),
            'djblog/post_detail.html',
        ))
       
        templates.extend(names)

        if self.object.template_name:
            templates.insert(0, self.object.template_name)

        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates


class GenericPostDetailView(PostBase, DetailView):
    """
    Detalle para un objecto generico /post_type_slug/slug
    """

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.get_for_lang()
        return Post.objects.get_generic_posts()

    def get_object(self):
        post_type_slug = self.kwargs.get('post_type_slug', '')
        slug = self.kwargs.get('slug', '')
        return get_object_or_404(self.get_queryset(), post_type__post_type_slug=post_type_slug, slug=slug)

    def get_template_names(self):
        names = super(GenericPostDetailView, self).get_template_names()
        post_type_slug = self.kwargs.get('post_type_slug', '')
        post_slug = self.kwargs.get('slug', '')
        domain = self.get_current_site().domain
        categories_site_templates = []
        categories_templates =[]
        templates = []

        obj = self.get_object()

        if obj.template_name:
            templates.append(obj.template_name)

        if self.post_type:
            post_type_slug = self.post_type.slug
            if self.post_type.template_name:
                templates.append(self.post_type.template_name)

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        for cat in self.object.category.all():
            categories_site_templates.append('djblog/%(domain)s/%(post_type)s/%(category)s/%(slug)s_post_detail.html' % \
                    dict(post_type=post_type_slug, domain=domain, category=cat.slug, slug=post_slug))

            categories_site_templates.append('djblog/%(domain)s/%(post_type)s/%(category)s/post_%(slug)s.html' % \
                    dict(post_type=post_type_slug, domain=domain, category=cat.slug, slug=post_slug))

            categories_site_templates.append('djblog/%(domain)s/%(post_type)s/%(category)s/post_detail.html' % \
                    dict(post_type=post_type_slug, domain=domain, category=cat.slug))

            categories_templates.append('djblog/%(post_type)s/%(category)s/%(slug)s_post_detail.html' % \
                    dict(post_type=post_type_slug, category=cat.slug, slug=post_slug))

            categories_templates.append('djblog/%(post_type)s/%(category)s/post_%(slug)s.html' % \
                    dict(post_type=post_type_slug, category=cat.slug, slug=post_slug))

            categories_templates.append('djblog/%(post_type)s/%(category)s/post_detail.html' % \
                    dict(post_type=post_type_slug, category=cat.slug))

        templates.extend(categories_site_templates)
        templates.extend((
            'djblog/%(domain)s/%(post_type)s/%(slug)s_post_detail.html' % \
                    dict(domain=domain, post_type=post_type_slug, slug=post_slug),
            'djblog/%(domain)s/%(post_type)s/post_%(slug)s.html' % \
                    dict(domain=domain, post_type=post_type_slug, slug=post_slug),
            'djblog/%(domain)s/%(post_type)s/post_detail.html' % \
                    dict(post_type=post_type_slug, domain=domain),
        ))
        
        templates.extend(categories_templates)
        templates.extend((
            'djblog/%(post_type)s/%(slug)s_post_detail.html' % \
                    dict(post_type=post_type_slug, slug=post_slug),
            'djblog/%(post_type)s/post_%(slug)s.html' % \
                    dict(post_type=post_type_slug, slug=post_slug),
            'djblog/%(post_type)s/post_detail.html' % \
                    dict(post_type=post_type_slug),
        ))
       
        templates.extend(names)

        if self.object.template_name:
            templates.insert(0, self.object.template_name)

        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates

    def get_context_data(self, **kwargs):
        """
        Agrega al `context` el `post_type`
        """
        logger.info("GenericPostDetailView -> get_context_data")

        post_type_slug = self.kwargs.get('post_type_slug', '')
        context = super(GenericPostDetailView, self).get_context_data(**kwargs)
        try:
            context['post_type'] = PostType.objects.get(post_type_slug=post_type_slug)
        except (PostType.DoesNotExist, PostType.MultipleObjectsReturned):
            logger.debug("PostType %s DoesNotExist or MultipleObjectsReturned", post_type_slug)
            pass

        self.post_type = context.get('post_type')
        return context



class GenericPostListView(PostBase, ListView):
    """
    Listado para un objecto generico /post_type_slug/
    """

    def get_queryset(self):
        post_type_slug = self.kwargs.get('post_type_slug', '')
        
        post_type = get_object_or_404(PostType, post_type_slug=post_type_slug)

        if self.request.user.is_staff:
            return Post.objects.get_for_lang().filter(post_type=post_type)
        return Post.objects.get_generic_posts(post_type=post_type)

    def get_template_names(self):
        names = super(GenericPostListView, self).get_template_names()
        domain = self.get_current_site().domain
        categories_site_templates = []
        categories_templates =[]
        templates = []

        post_type_slug = self.kwargs.get('post_type_slug', '')

        if self.post_type:
            post_type_slug = self.post_type.slug
            if self.post_type.template_name:
                templates.append(self.post_type.template_name)

        if self.template_name:
            names.remove(self.template_name)
            templates.append(self.template_name)

        templates.extend(categories_site_templates)
        templates.extend((
            'djblog/%(domain)s/%(post_type)s/post_list.html' % \
                    dict(post_type=post_type_slug, domain=domain),
        ))
        
        templates.extend(categories_templates)
        templates.extend((
            'djblog/%(post_type)s/post_list.html' % \
                    dict(post_type=post_type_slug),
        ))
       
        templates.extend(names)
        logger.debug('Loading theses templates names: \n%s', "\n".join(templates))
        return templates

    def get_context_data(self, **kwargs):
        """
        Agrega al `context` el `post_type`
        """
        logger.info("GenericPostListView -> get_context_data")

        post_type_slug = self.kwargs.get('post_type_slug', '')
        context = super(GenericPostListView, self).get_context_data(**kwargs)
        try:
            context['post_type'] = PostType.objects.get(post_type_slug=post_type_slug)
        except (PostType.DoesNotExist, PostType.MultipleObjectsReturned):
            logger.debug("PostType %s DoesNotExist or MultipleObjectsReturned", post_type_slug)
            pass

        self.post_type = context.get('post_type')
        return context


class GenericCategoryListView(GenericPostListView):
    """
    Listado para un objecto generico por categoría /post_type_slug/category/category_slug/
    """
    def get_queryset(self):
        qs = super(GenericCategoryListView, self).get_queryset()
        category_slug = self.kwargs.get('slug', '')
        return qs.filter(Q(category__slug=category_slug)|Q(category__parent__slug=category_slug)).distinct()

    def get_context_data(self, **kwargs):
        """
        Agrega al `context` la `category`
        """

        category_slug = self.kwargs.get('slug', '')
        context = super(GenericCategoryListView, self).get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=category_slug)
        except (Category.DoesNotExist, Category.MultipleObjectsReturned):
            logger.debug("Category %s DoesNotExist or MultipleObjectsReturned", category_slug)
            pass

        self.category = context.get('category')
        return context
