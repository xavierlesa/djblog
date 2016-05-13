# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
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
                ('name', models.CharField(max_length=140, verbose_name='T\xedtulo')),
                ('level', models.PositiveSmallIntegerField(default=0)),
                ('blog_category', models.BooleanField(default=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('show_on_list', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('level', '-pub_date', 'name'),
                'verbose_name': 'Categor\xeda',
                'verbose_name_plural': 'Categor\xedas',
            },
        ),
        migrations.CreateModel(
            name='CategoryRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_category', models.ForeignKey(related_name='from_category', to='djblog.Category')),
                ('to_category', models.ForeignKey(related_name='to_category', to='djblog.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.PositiveIntegerField()),
                ('key', models.SlugField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('text_field', models.TextField()),
                ('rich_field', models.BooleanField(default=False, help_text='Este estado determina si se mostrara como texto enriquecido o plano')),
                ('sort_order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='Post',
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
                ('title', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('copete', models.TextField(help_text='Es opcional, y si exsite se usa para el extracto', verbose_name='Copete', blank=True)),
                ('content', models.TextField(verbose_name='Contenido en texto plano')),
                ('content_rendered', models.TextField(help_text='Este es el contenido a mostrarse, permite marcado', verbose_name='Contenido HTML')),
                ('template_name', models.CharField(help_text='Define un template para este objeto (post o p\xe1gina).                     path/al/template/nombre_template.html', max_length=200, null=True, blank=True)),
                ('custom_template', models.TextField(null=True, verbose_name='Template HTML/Daango', blank=True)),
                ('publication_date', models.DateTimeField(verbose_name='Fecha de publicaci\xf3n')),
                ('expiration_date', models.DateTimeField(null=True, verbose_name='Fecha de vencimiento', blank=True)),
                ('sort_order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('allow_comments', models.NullBooleanField(default=True, verbose_name='Permitir comentarios')),
                ('comments_finish_date', models.DateTimeField(null=True, verbose_name='Cerrar autom\xe1ticamente', blank=True)),
                ('author', models.ForeignKey(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ManyToManyField(to='djblog.Category', null=True, blank=True)),
            ],
            options={
                'ordering': ('-sort_order', '-publication_date', 'title'),
                'get_latest_by': 'publication_date',
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
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
                ('template_name', models.CharField(help_text='Define un template para este objeto (post o p\xe1gina).                     path/al/template/nombre_template.html', max_length=200, null=True, blank=True)),
                ('custom_template', models.TextField(null=True, verbose_name='Template HTML/Daango', blank=True)),
                ('post_type_name', models.CharField(help_text='Determina el uso y comportamiento del Post, \n                    siendo `Post` y `P\xe1gina` los reservados y por defecto.', max_length=100, verbose_name='Tipo de objeto')),
                ('post_type_slug', models.SlugField(help_text='Importante para determinar el inicio de URL. \n                    Ej: Para el `slug` `autos` \n                    /post_type_slug/slug/ -> /autos/peugeot-208/', verbose_name='Slug del tipo')),
                ('site', models.ManyToManyField(related_name='djblog_posttype_related', null=True, to='sites.Site', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140, verbose_name='Nombre o T\xedtulo')),
                ('description', models.TextField(verbose_name='Descripci\xf3n', blank=True)),
                ('is_public', models.BooleanField(default=False, help_text='Este estado determina si una publicaci\xf3n es visible o no')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.CreateModel(
            name='Tag',
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
                ('name', models.CharField(unique=True, max_length=64)),
                ('site', models.ManyToManyField(related_name='djblog_tag_related', null=True, to='sites.Site', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Etiqueta',
                'verbose_name_plural': 'Etiquetas',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.ForeignKey(to='djblog.PostType'),
        ),
        migrations.AddField(
            model_name='post',
            name='related',
            field=models.ManyToManyField(related_name='_post_related_+', verbose_name='Contenido relacionado', to='djblog.Post', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='site',
            field=models.ManyToManyField(related_name='djblog_post_related', null=True, to='sites.Site', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.ForeignKey(blank=True, to='djblog.Status', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(help_text='Tags descript\xedvos', to='djblog.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ManyToManyField(related_name='children', null=True, through='djblog.CategoryRelationship', to='djblog.Category', blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='site',
            field=models.ManyToManyField(related_name='djblog_category_related', null=True, to='sites.Site', blank=True),
        ),
    ]
