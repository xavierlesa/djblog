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
from mediacontent.admin import MediaContentInline
from djblog.models import Post, PostType, Category, Status, Tag
#from djblog.forms import PostAdminForm
from djblog.content_extra.admin import ExtraContentInline
from djblog.common.admin import BaseAdmin


class PostTypeAdmin(BaseAdmin):
    list_display = (
            'id',
            'post_type_name',
            'post_type_slug',
            'slug',
            'lang', 
            'get_site',
            )

    list_display_links = (
            'id',
            'post_type_name',
            )

    list_filter = (
            'post_type_name', 
            ) + BaseAdmin.list_filter

    search_fields = [
            'post_type_name', 
            ]

    prepopulated_fields = {
            'slug': (
                'post_type_name',
                ),
            'post_type_slug': (
                'post_type_name',
                ),
            }

    fieldsets = (
            (None, {
                'fields': (
                    'post_type_name', 
                    'post_type_slug', 
                    (
                        'site', 
                        'lang', 
                        ),
                    'slug',
                    )
                }),
            ('Templates', {
                'fields':  (
                    'template_name',
                    'custom_template',
                    ),
                'classes': (
                    'collapse',
                    'select-template',
                    )
                }),
            )


class PostAdmin(BaseAdmin):
    #form = PostAdminForm

    inlines = [
            MediaContentInline, 
            ExtraContentInline
            ]

    list_display = (
            'id',
            'title', 
            'slug',
            'status', 
            'get_publication_date', 
            'get_expiration_date', 
            'get_is_active', 
            'post_type', 
            'author', 
            'get_category', 
            'lang',
            'get_site',
            )

    list_display_links = (
            'title',
            )

    list_filter = (
            'post_type',
            'category', 
            'author', 
            ) + BaseAdmin.list_filter

    search_fields = [
            'title', 
            'copete', 
            'content'
            ]

    prepopulated_fields = {
            'slug': (
                'title',
                ),
            }

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
                (None, {
                    'fields': (
                        'title', 
                        'slug', 
                        'copete', 
                        'content', 
                        'content_rendered', 
                        'category', 
                        (
                            'post_type',
                            'status', 
                            'author'
                            ),
                        (
                            'site', 
                            'lang', 
                            ),
                        )
                    }),
                ('Templates', {
                    'fields':  (
                        'template_name',
                        'custom_template',
                        ),
                    'classes': (
                        'collapse',
                        'select-template',
                        )
                    }),
                )

        return super(PostAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context={}):
        self.fieldsets = (
                (None, {
                    'fields': (
                        'title', 
                        'slug', 
                        'copete', 
                        'content',
                        'content_rendered', 
                        'category', 
                        (
                            'post_type',
                            'status', 
                            'author'
                            ),
                        (
                            'site', 
                            'lang', 
                            ),
                        )
                    }),
                ('Templates', {
                    'fields':  (
                        'template_name',
                        'custom_template',
                        ),
                    'classes': (
                        'collapse',
                        'select-template',
                        )
                    }),
                ('Comments', {
                    'fields': (
                        'allow_comments', 
                        'comments_finish_date'
                        ),
                    'classes': (
                        'collapse',
                        )
                    }),
                ('Scheduling', {
                    'fields': (
                        (
                            'publication_date', 
                            'expiration_date'
                            ),
                        ),
                    'classes': (
                        'collapse',
                        )
                    }),
                ('Relationships', {
                    'fields': (
                        (
                            #'followup_for', 
                            'related'
                            ), 
                        'tags'
                        ),
                    'classes': (
                        'collapse',
                        )
                    }),
                ) + BaseAdmin.fieldsets

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
    list_display = (
            'name', 
            'parent', 
            'level', 
            'get_blog_category', 
            'get_is_active', 
            'get_site'
            )

    list_filter = (
            'level',
            'blog_category',
            'site'
            ) + BaseAdmin.list_filter

    prepopulated_fields = {
            'slug': (
                'name',
                )
            } 

    fieldsets = (
            (None, {
                'fields': (
                    'name', 
                    'slug', 
                    'show_on_list', 
                    'parent', 
                    'description', 
                    'site'
                    )
                }),
            ('Advanced', {
                'fields': (
                    'blog_category', 
                    'level'
                    ),
                'classes': (
                    'collapse',
                    )
                }),
            ) + BaseAdmin.fieldsets

    def get_blog_category(self, obj):
        if obj.blog_category:
            return u'de Blog'
        return u'No de Blog'
    get_blog_category.short_description = u'categoría de blog'
    get_blog_category.allow_tags = True




class StatusAdmin(admin.ModelAdmin):
    list_display = (
            'name', 
            'description', 
            'get_is_public'
            )

    def get_is_public(self, obj):
        if obj.is_public:
            return u'Público'
        return u'Borrador'
    get_is_public.short_description = u'es público'
    get_is_public.allow_tags = True



class TagAdmin(BaseAdmin):
    list_display = (
            'name', 
            'get_is_active', 
            'get_site',
            )

    list_filter = (
            'is_active', 
            'site',
            )

    prepopulated_fields = {
            'slug': (
                'name',
                )
            }

    fieldsets = (
            (None, {
                'fields': (
                    'name', 
                    'slug'
                    )
                }),
            ) + BaseAdmin.fieldsets



admin.site.register(PostType, PostTypeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Tag, TagAdmin)
