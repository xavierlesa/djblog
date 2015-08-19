# *-* coding=utf-8 *-*

"""
Este es un grupo de aplicaciones desarrolladas para funcionar en conjunto
pero también de forma independiente. Ideada para usarse como Blog, CMS, Portal
o Red Social y/u otro fin que se le quiera dar, no hace cafe :(

Author: Xavier Lesa <xavierlesa@gmail.com>
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.http import HttpResponse
from djblog.common.models import MultiSiteBaseModel

import logging
logger = logging.getLogger(__name__)

class MultiSiteBaseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return self.model.objects_for_admin.get_queryset()

    def get_site(self, obj):
        return u", ".join([s.name for s in obj.site.all()])

    get_site.short_description = u"Sites"

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    try:
    #        qs = db_field.rel.related_model.objects_for_admin
    #    except:
    #        logger.debug("Error objects_for_admin no existe en el field %s", db_field)
    #        pass
    #    else:
    #        kwargs["queryset"] = qs.all()
    #        logger.debug("QuerySet para el field %s", db_field)

    #    return super(MultiSiteBaseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    #
    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    try:
    #        qs = db_field.rel.related_model.objects_for_admin
    #    except:
    #        logger.debug("Error objects_for_admin no existe en el field %s", db_field)
    #        pass
    #    else:
    #        kwargs["queryset"] = qs.all()
    #        logger.debug("QuerySet para el field %s", db_field)

    #    return super(MultiSiteBaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BaseAdmin(MultiSiteBaseAdmin):
    save_on_top = True
    save_as = True
    date_hierarchy = 'pub_date'
    
    list_display = (
            'get_is_public',
            )

    list_filter = (
            'pub_date', 
            'up_date', 
            'is_active', 
            'get_site'
            )

    list_filter = (
            'pub_date', 
            'up_date', 
            'is_active'
            )
    
    list_filter_advanced = (
            'pub_date', 
            'up_date', 
            'is_active', 
            'is_live', 
            'lang', 
            'site'
            )
    
    fieldsets = (
            ('Seo Meta config.', {
                'fields': (
                    'meta_keywords', 
                    'meta_description',
                    ),
                'classes': (
                    'collapse',
                    )
                }),
            ('Advanced config.', {
                'fields': (
                    'pub_date', 
                    'is_active', 
                    'is_live', 
                    'lang',
                    ),
                'classes': (
                    'collapse',
                    )
                }),
            )

    def get_is_active(self, obj):
        if obj.is_active:
            return u'Activo'

        return u'No Activo' 

    get_is_active.short_description = u'activo'
    get_is_active.allow_tags = True


def export_selected(modeladmin, request, queryset):
    app, module, fields = modeladmin.model._meta.app_label, modeladmin.model._meta.model_name, modeladmin.model._meta.fields
    qs = queryset
    csv_data = "\t".join([u"%s" % f.name for f in fields]) + "\r\n"

    for data in qs:
        csv_data = csv_data + "\t".join([u"%s" % d for d in [getattr(data, f.name) for f in fields]]) + "\r\n"

    response = HttpResponse(csv_data, mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename=%s-%s.xls" % (app, module) 

    return response
export_selected.short_description = u"Export Selected"
admin.site.add_action(export_selected)
