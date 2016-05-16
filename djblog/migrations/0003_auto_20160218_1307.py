# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0002_auto_20150803_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extracontent',
            options={'ordering': ('sort_order', 'name')},
        ),
        migrations.AddField(
            model_name='extracontent',
            name='sort_order',
            field=models.PositiveIntegerField(default=1, verbose_name='Orden'),
        ),
    ]
