from django import forms
from django.db import models
from django.contrib.contenttypes.admin import GenericStackedInline
from djblog.content_extra.models import ExtraContent
from redactor.widgets import RedactorEditor

class ExtraContentInline(GenericStackedInline):
    model = ExtraContent
    ct_field = 'content_type'
    ct_fk_field = 'object_pk'
    verbose_name = "Field Extra"
    verbose_name_plural = "Fields Extra"
    
    extra = 1
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'cols':40, 'rows':4})} }
    verbose_name = u"extra field"
    """
    fieldsets = (
        ('Extra Content', {
            'fields': ('key', 'name', 'field'),
            'classes': ('collapse',)
        }),
    )
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text_field':
            kwargs['widget'] = RedactorEditor()
        return super(ExtraContentInline,self).formfield_for_dbfield(db_field,**kwargs)
