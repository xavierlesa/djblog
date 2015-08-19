# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extracontent',
            old_name='field',
            new_name='text_field',
        ),
        migrations.AddField(
            model_name='extracontent',
            name='rich_field',
            field=models.BooleanField(default=False, help_text='Este estado determina si se mostrara como texto enriquecido o plano'),
        ),
    ]
