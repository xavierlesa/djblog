# *-* coding=utf-8 *-*

"""
Nebula es un grupo de aplicaciones desarrolladas para funcionar en conjunto
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
    #def __init__(self, *args, **kwargs):
    #    super(BaseAdmin, self).__init__(*args, **kwargs)
    #    app, module, fields = args[0]._meta.app_label, args[0]._meta.module_name, [f.name for f in args[0]._meta.fields]

    #    return super(BaseAdmin, self).__init__(*args, **kwargs)

    save_on_top = True
    save_as = True
    date_hierarchy = 'pub_date'
    
    list_display = ('get_is_public',)
    list_filter = ('pub_date', 'up_date', 'is_active', 'get_site')
    list_filter = ('pub_date', 'up_date', 'is_active')
    
    list_filter_advanced = ('pub_date', 'up_date', 'is_active', 'is_live', 'lang', 'site')
    
    fieldsets = (
        ('Seo Meta config.', {
            'fields': ('meta_keywords', 'meta_description',),
            'classes': ('collapse',)
        }),
        ('Advanced config.', {
            'fields': ('pub_date', 'is_active', 'is_live', 'lang', ),
            'classes': ('collapse',)
        }),
    )

    def get_is_active(self, obj):
        if obj.is_active:
            return u'Activo' #mark_safe('<img src="%(media)simg/admin/accept.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=False))
        return u'No Activo' #mark_safe('<img src="%(media)simg/admin/cross.png" alt="%(alt)s" />' % dict(media=settings.MEDIA_URL, alt=False))
    get_is_active.short_description = u'activo'
    get_is_active.allow_tags = True

    #def get_site(self, obj):
    #    return u", ".join([s.name for s in obj.site.all()])

def export_selected(modeladmin, request, queryset):
    app, module, fields = modeladmin.model._meta.app_label, modeladmin.model._meta.module_name, modeladmin.model._meta.fields
    qs = queryset
    csv_data = "\t".join([u"%s" % f.name for f in fields]) + "\r\n"
    for data in qs:
        csv_data = csv_data + "\t".join([u"%s" % d for d in [getattr(data, f.name) for f in fields]]) + "\r\n"
    response = HttpResponse(csv_data, mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename=%s-%s.xls" % (app, module) 
    return response
export_selected.short_description = u"Export Selected"
admin.site.add_action(export_selected)
