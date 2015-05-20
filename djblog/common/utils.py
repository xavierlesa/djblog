# *-* coding:utf8 *-*

from django.conf.urls import patterns, url, include
from django.contrib.sites.models import Site
from django.template.loader import select_template
#from django.utils.timezone import now as tz_now, get_current_timezone, utc

def _get_template(template_list):
    """
    resuelve el template por site
    """
    site = Site.objects.get_current().name
    t = map(lambda x: u"%s/%s" % (site, x), template_list)
    s = select_template(t).name
    return s


#def convert_to_localtime(date):
#    if not date.tzinfo:
#        date = date.replace(tzinfo=utc)
#    tz = get_current_timezone()
#    return tz.normalize(date.astimezone(tz))

"""
ver como hace el Loader, para usarlo directamente desde nuesgtro propio loader
https://code.djangoproject.com/browser/django/trunk/django/template/loaders/app_directories.py
"""
