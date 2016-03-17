# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0006_auto_20160225_2012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-sort_order', '-publication_date', 'title'), 'get_latest_by': 'publication_date', 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AddField(
            model_name='post',
            name='sort_order',
            field=models.PositiveIntegerField(default=1, verbose_name='Orden'),
        ),
    ]
