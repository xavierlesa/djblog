# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0002_auto_20150520_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='template_name',
            field=models.CharField(help_text='Define un template para este objeto (post o p\xe1gina).                     path/al/template(nombre_template.html', max_length=200, null=True, blank=True),
        ),
    ]
