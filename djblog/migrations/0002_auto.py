# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import logging
logger = logging.getLogger(__name__)

def create_default_postyypes(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    # Hack horrible!
    try:
        PostType = apps.get_model('djblog', 'PostType')
    except LookupError:
        from djblog.models import PostType

    PostType.objects.using(db_alias).get_or_create(post_type_name="Blog", post_type_slug="blog")
    PostType.objects.using(db_alias).get_or_create(post_type_name="Page", post_type_slug="page")
    

def create_default_post_status(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    # Hack horrible!
    try:
        Status = apps.get_model('djblog', 'Status')
    except LookupError:
        from djblog.models import Status

    Status.objects.using(db_alias).get_or_create(name="public", is_public=True)
    Status.objects.using(db_alias).get_or_create(name="draft", is_public=False)



class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0001_initial'),            
    ]

    operations = [
        migrations.RunPython(create_default_postyypes),
        migrations.RunPython(create_default_post_status),
    ]
