# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0003_auto_20150520_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Contenido en texto plano'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_rendered',
            field=models.TextField(help_text='Este es el contenido a mostrarse, permite marcado', verbose_name='Contenido HTML'),
        ),
        migrations.AlterField(
            model_name='post',
            name='copete',
            field=models.TextField(help_text='Es opcional, y si exsite se usa para el extracto', verbose_name='Copete', blank=True),
        ),
    ]
