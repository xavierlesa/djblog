# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0009_auto_20160516_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='post',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='post',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='posttype',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='posttype',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='meta_keywords',
        ),
        migrations.AddField(
            model_name='category',
            name='seo_description',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_keywords',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_title',
            field=models.CharField(help_text='opcional, para el SEO', max_length=70, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='seo_description',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='seo_keywords',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='seo_title',
            field=models.CharField(help_text='opcional, para el SEO', max_length=70, blank=True),
        ),
        migrations.AddField(
            model_name='posttype',
            name='seo_description',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='posttype',
            name='seo_keywords',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='posttype',
            name='seo_title',
            field=models.CharField(help_text='opcional, para el SEO', max_length=70, blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='seo_description',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='seo_keywords',
            field=models.TextField(help_text='opcional, para el SEO', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='seo_title',
            field=models.CharField(help_text='opcional, para el SEO', max_length=70, blank=True),
        ),
    ]
