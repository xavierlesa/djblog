# *-* coding=utf-8 *-*

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.forms.widgets import flatatt
from django.utils.encoding import smart_unicode, force_unicode
from django.template.loader import render_to_string
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe

from djblog.models import Post, Category

class PreviewContentWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is None: 
            value = ''
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        context = { 
            'id':final_attrs['id'], 
            'id_content':final_attrs['id_content'], 
            'attrs':flatatt(final_attrs), 
            'content':value, 
            'name': name,
            'STATIC_URL':settings.STATIC_URL
        }

        return mark_safe(render_to_string('djeditor/djeditor_widget.html', context))




class PostAdminForm(forms.ModelForm):
    #slug = forms.SlugField(required=False)
    content_rendered = forms.CharField(widget=PreviewContentWidget(attrs={'id_content':'id_content'}), required=False)
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            obj = kwargs['instance']

            #self.fields['category'].queryset = Category.objects.filter(blog_category = not obj.is_page)


    class Meta:
        model = Post
        exclude = []
