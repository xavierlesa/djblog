# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_djblog_defaults(apps, schema_editor):
    PostType = apps.get_model("djblog", "PostType")
    db_alias = schema_editor.connection.alias
    PostType.objects.using(db_alias).bulk_create([
        PostType(post_type_name="Blog", post_type_slug="blog"),
        PostType(post_type_name="Page", post_type_slug="page"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('djblog', '0004_auto_20150522_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(blank=True, max_length=20, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('pub_date', models.DateTimeField(verbose_name='Fecha de creaci\xf3n', blank=True)),
                ('up_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizaci\xf3n')),
                ('slug', models.SlugField(max_length=250)),
                ('is_active', models.BooleanField(default=True, help_text='activa para usar en el frontend', verbose_name='Es activo')),
                ('is_live', models.BooleanField(default=True, help_text='NO activo lo hace -invisible-', verbose_name='Es visible')),
                ('meta_keywords', models.TextField(help_text='opcional, para el SEO', blank=True)),
                ('meta_description', models.TextField(help_text='opcional, para el SEO', blank=True)),
                ('post_type_name', models.CharField(help_text='Determina el uso y comportamiento del Post, \n                    siendo `Post` y `P\xe1gina` los reservados y por defecto.', max_length=100, verbose_name='Tipo')),
                ('post_type_slug', models.SlugField(help_text='Importante para determinar el inicio de URL. \n                    Ej: Para el `slug` `autos` \n                    /post_type_slug/slug/ -> /autos/peugeot-208/', verbose_name='Slug')),
                ('template_name', models.CharField(help_text='Define un template para este objeto (post o p\xe1gina).                     path/al/template(nombre_template.html', max_length=200, null=True, blank=True)),
                ('custom_template', models.TextField(null=True, verbose_name='Template HTML/Daango', blank=True)),
                ('site', models.ManyToManyField(related_name='djblog_posttype_related', null=True, to='sites.Site', blank=True)),
            ],
            options={
                'ordering': ('-pub_date', '-up_date'),
                'abstract': False,
            },
        ),
        migrations.RunPython(add_djblog_defaults),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publication_date', 'title'), 'get_latest_by': 'publication_date', 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='followup_for',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_page',
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.ForeignKey(default=1, to='djblog.PostType'),
            preserve_default=False,
        ),
    ]
