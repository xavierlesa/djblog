# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0003_auto_20160218_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extracontent',
            options={'ordering': ('sort_order',)},
        ),
    ]
