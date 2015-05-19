# *-* coding=utf-8 *-*

from datetime import datetime
from django import forms
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.template.defaultfilters import timesince, timeuntil
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.safestring import mark_safe
from nebula.djblog.models import Post, Category, Status, Tag
from nebula.djblog.forms import PostAdminForm
from nebula.mediacontent.admin import MediaContentInline
from nebula.djblog.content_extra.admin import ExtraContentInline
from nebula.common.admin import BaseAdmin

NEBULA_FLAGS = getattr(settings, 'NEBULA_FLAGS', {})

class PostAdmin(BaseAdmin):
    list_display = ('get_category', 'title', 'status', 'author', 'get_publication_date', 'get_expiration_date', 'get_is_active', 'get_is_page', 'get_site')
    list_display_links = ('title',)
    list_filter = ('category', 'author', 'is_page').__add__(BaseAdmin.list_filter)
    search_fields = ['title', 'copete', 'content']
    form = PostAdminForm
    inlines = [MediaContentInline, ExtraContentInline]
    prepopulated_fields = {'slug': ('title',),}

    # solo mostrar los objetos del usuario, o todo si es superuser
    def queryset(self, request):
        qs = super(PostAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(models.Q(user=request.user)|models.Q(author=request.user))

    # quien crea siempre es el user logeado
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        try:
            form.save_m2m()
        except:
            pass
        return super(PostAdmin, self).save_model(request, obj, form, change)


    def add_view(self, request, form_url='', extra_context={}):
        self.fieldsets = (
            (None, {'fields': ('title', 'slug', 'copete', 'content_rendered', 'category', 'site', ('is_page', 'status', 'author'))}),
        )
        return super(PostAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context={}):
        self.fieldsets = (
            (None, {'fields': ('title', 'slug', 'copete', 'content_rendered', 'category', 'site', ('is_page', 'status', 'author'))}),
            ('Comments', {
                'fields': ('allow_comments', 'comments_finish_date'),
                'classes': ('collapse',)
            }),
            ('Scheduling', {
                'fields': (('publication_date', 'expiration_date'),),
                'classes': ('collapse',)
            }),
            ('Relationships', {
                'fields': (('followup_for', 'related'), 'tags'),
                'classes': ('collapse',)
            }),
        ).__add__(BaseAdmin.fieldsets)
        return super(PostAdmin, self).change_view(request, object_id, extra_context=extra_context)


    def get_expiration_date(self, obj):
        if not obj.expiration_date:
            return mark_safe('<span style="color:green">nunca expira</span>')

        if obj.expiration_date and obj.expiration_date <= timezone.now():
            return mark_safe('<span style="color:orange">expiro hace %s</span>' % timesince(obj.expiration_date))
        return mark_safe('<span style="color:green">expira en %s</span>' % timeuntil(obj.expiration_date))
    get_expiration_date.allow_tags = True
    get_expiration_date.short_description = _(u"expiration_date")

    def get_publication_date(self, obj):
        if obj.publication_date and obj.publication_date <= timezone.now():
            return mark_safe('<span style="color:green">publicado hace %s</span>' % timesince(obj.publication_date))
        return mark_safe('<span style="color:blue">se publica en %s</span>' % timeuntil(obj.publication_date))
    get_publication_date.allow_tags = True
    get_publication_date.short_description = _(u"publication_date")

    def get_is_page(self, obj):
        if obj.is_page:
            return u'Página' #mark_safe(u'<img src="%simg/admin/page.png" title="Página" alt="Página" />' % settings.MEDIA_URL)
        elif obj.category.noblog():
            return u'Post no de blog' #mark_safe(u'<img src="%simg/admin/noblog-post.png" title="no blog post" alt="no blog post" />' % settings.MEDIA_URL)
        return u'Post del blog'
    get_is_page.short_description = u'(no)blog post o página'
    get_is_page.allow_tags = True

    def get_category(self, obj):
        return ', '.join([c.name for c in obj.category.all()])
    get_category.short_description = _(u'In Category')
 
    def get_tags(self, obj):
        return ', '.join([c.name for c in obj.tags.all()])
    get_tags.short_description = _(u'Tags')

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = _(u'Mark select articles as active')

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = _(u'Mark select articles as inactive')




class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'parent', 'level', 'get_blog_category', 'get_is_active', 'get_site')
    list_filter = ('level','blog_category','site',).__add__(BaseAdmin.list_filter)
    prepopulated_fields = {'slug': ('name',)} 
    _main_fields = (None, {'fields': ('name', 'slug', 'parent', 'site')})
    if NEBULA_FLAGS.get('BLOG_CATEGORY_DESCRIPTION', False):
        _main_fields = (None, {'fields': ('name', 'slug', 'description', 'parent', 'site')})
    if NEBULA_FLAGS.get('BLOG_CATEGORY_SHOW_LIST', False):
        _main_fields[1]['fields'] = _main_fields[1]['fields'] + ('show_on_list', )

    fieldsets = (
        _main_fields,
        ('Advanced', {
            'fields': ('blog_category', 'level'),
            'classes': ('collapse',)
        }),

    ).__add__(BaseAdmin.fieldsets)

    def get_blog_category(self, obj):
        if obj.blog_category:
            return u'de Blog' #mark_safe('<img src="%(media)simg/admin/accept.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=True))
        return u'No de Blog' #mark_safe('<img src="%(media)simg/admin/cross.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=True))
    get_blog_category.short_description = u'categoría de blog'
    get_blog_category.allow_tags = True




class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_is_public')

    def get_is_public(self, obj):
        if obj.is_public:
            return u'Público' #mark_safe('<img src="%(media)simg/admin/accept.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=True))
        return u'Borrador' #mark_safe('<img src="%(media)simg/admin/cross.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=True))
    get_is_public.short_description = u'es público'
    get_is_public.allow_tags = True



class TagAdmin(BaseAdmin):
    list_display = ('name', 'get_is_active', 'get_site',)
    list_filter = ('is_active', 'site',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
    ).__add__(BaseAdmin.fieldsets)



admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Tag, TagAdmin)
