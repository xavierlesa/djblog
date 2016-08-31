# -*- coding:utf-8 -*-
"""
Herramienta para migrar los djblog viejos de nebula al nuevo sistema.

Importa desde un json (el que dumpea django dumpdata) y crea una abstracción
para cada clase y finalmente crea el objecto (sync)

import json
from djblog.djblog_migration_utility import *

file_data = open('djblog_dumpdata.json', 'rb')
file_data = json.loads(file_data.readline())

categories = {}

for cat in file_data:
    if cat['model'] == 'djblog.category':
        print cat['model']
        categories.update({cat['pk']: cat['fields']})


"""

import os
import datetime
import urllib2
import json
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files.images import ImageFile
from djblog.models import Post, PostType, Category, Tag, MediaContent, ExtraContent

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
import logging
log = logging.getLogger(__name__)

ct_post = ContentType.objects.get_for_model(Post)

class DjblogImporterException(Exception):
    pass


class FieldsAbstract(object):
    fields = []


class ItemAttributeAbstract(FieldsAbstract):

    def __init__(self, data, *args, **kwargs):
        for field, attribute in data.iteritems():
            setattr(self, field, attribute)


class ImportAttributesAbstract(FieldsAbstract):
    items = []

    def __init__(self, data, item_class=ItemAttributeAbstract, *args, **kwargs):
        """
        Espera un dict con los campos del post y lo transforma en propiedades
        de la clase.

        """

        if isinstance(data, (list, tuple)):
            for item in data:
                self.items.append( item_class(item) )

        elif isinstance(data, dict):
            for field, attribute in data.iteritems():
                #print("setting {0}".format(field))
                setattr(self, field, attribute)

    def __iter__(self):
        for item in self.items:
            yield item


class DjblogCategory(ImportAttributesAbstract):

    prefix = u'migración'

    def validate(self):
        create = False

        try:
            category = Category.objects.get(slug=self.slug)
        except Category.DoesNotExist:
            category = Category(name=u"[{0}] {1}".format(self.prefix, self.name), slug=self.slug)
            create = True

        return category, create

    
    def sync(self, *args, **kwargs):
        try:
            category = Category.objects.get(slug=self.slug)
        except Category.DoesNotExist:
            category = Category.objects.create(name=u"[{0}] {1}".format(self.prefix, self.name), slug=self.slug)

        self.category = category
        return self.category


class DjblogTag(ImportAttributesAbstract):
    
    def sync(self, *args, **kwargs):
        try:
            tag = Tag.objects.get(slug=self.slug)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=self.name, slug=self.slug)

        self.tag = tag
        return self.tag


class DjblogExtraContent(ImportAttributesAbstract):
    
    def sync(self):
        ec = ExtraContent(content_type=ct_post, field=self.field, 
                key=self.key, name=self.name, object_pk=self.object_pk)
        ec.save()
        self.extra_content = ec
        return self.extra_content


class DjblogMediaContent(ImportAttributesAbstract):

    def download(self):
        import os
        os.system("scp -P 31755 xavier@devlinkb1://home/worklift/worklift/media/{0} tmp/".format(self.content))
        return "tmp/".format(self.content)

    def sync(self):
        mc = MediaContent.objects.filter(content_type=ct_post, object_pk=self.object_pk, title=self.title)

        # Solo si ya no tiene una imagen asociada entonces, asocia una
        if not mc:

            try:
                # baja la imagen asociada
                media_file = self.download()
            except:
                raise DjblogImporterException("Error al descargar el archivo {0}".format(self.content))
            else:

                try:
                    m = MediaContent(content_type=ct_post, object_pk=self.object_pk, 
                            title=self.title, description=self.description, 
                            pub_date=self.pub_date)

                    print u"Asocia el archivo {0} al post {1}".format(media_file, self.object_pk)
                    m.content.save(media_file, ImageFile(open(media_file, 'r')))
                    log.info("Archivo cargado/actualizado %s", media_file)
                    log.info("Elimina el archivo temporal %s", media_file)
                    try:
                        os.remove(media_file)
                    except (OSError, ValueError):
                        log.warning("ERROR al eliminar el archivo temporal %s", media_file)
                        pass

                except IOError:
                    log.info("IOError")
                
                except DjblogImporterException:
                    pass



class DjblogPost(ImportAttributesAbstract):
    id = None
    post_type = 'blog'
    _author = User.objects.get(pk=1)

    def __repr__(self):
        return "<DjblogPost ID:{0} \"{1}...\">".format(self.id, self.slug)


    # Author
    def set_author(self, data):
        pass
    def get_author(self):
        return self._author
    author = property(get_author, set_author)


    # Category
    def get_category(self):
        return self._category

    def set_category(self, data):
        self._category = [DjblogCategory(category) for category in data]
    category = property(get_category, set_category)

    
    # Tag
    def get_post_tag(self):
        return self.terms.get_post_tag()

    def set_post_tag(self, data):
        self.terms.set_post_tag(data)
    tags = property(get_post_tag, set_post_tag)

    def get_tags(self):
        return self._tags

    def set_tags(self, data):
        """
        Espera una lista con los tags asociadas al post
        """
        
        self._tags = [DjblogTag(tag) for tag in data]
    tags = property(get_tags, set_tags)


    def validate(self):
        create = False

        try:
            post_type = PostType.objects.get(post_type_slug=self.post_type)
        except:
            raise DjblogImporterException("No es posible asignar un <post_type>, está self.post_type vacio?")

        try:
            post = Post.objects.get(slug=self.slug, post_type=post_type)
        except Post.DoesNotExist:
            post = Post(title=self.title, slug=self.slug, 
                    content=self.content, content_rendered=self.content, 
                    pub_date=self.pub_date, publication_date=self.publication_date,
                    post_type=post_type)

            create = True

        return post, create


    def sync(self, *args, **kwargs):
        try:
            post_type = PostType.objects.get(post_type_slug=self.post_type)
        except:
            raise DjblogImporterException("No es posible asignar un <post_type>, está self.post_type vacio?")
            #post_type = PostType.objects.create(post_type_slug=self.post_type, 
            #        post_type_name=self.post_type)

        try:
            post = Post.objects.get(slug=self.slug, post_type=post_type)
        except Post.DoesNotExist:
            post = Post.objects.create(title=self.title, slug=self.slug, 
                    content=self.content, content_rendered=self.content, 
                    pub_date=self.pub_date, publication_date=self.publication_date,
                    post_type=post_type)

        self.post = post

        if not self.post.author:
            self.post.author = self.author

        ## sync categories
        #for category in self.categories:
        #    category.sync()
        #    
        #    self.post.category.add(category.category)

        ## sync tags
        #for tag in self.tags:
        #    tag.sync()
        #    
        #    self.post.tags.add(tag.tag)

        #if self.media_content.source:

        #    ct = ContentType.objects.get_for_model(self.post)
        #    mc = MediaContent.objects.filter(content_type=ct, object_pk=self.post.pk, title=self.media_content.title)

        #    # Solo si ya no tiene una imagen asociada entonces, asocia una
        #    if not mc:

        #        try:
        #            # baja la imagen asociada
        #            media_file = self.media_content.source.download()
        #        except urllib2.HTTPError:
        #            pass
        #            #raise DjblogImporterException("Error de codificación al descargar el archivo")
        #        else:

        #            try:
        #                m = MediaContent(content_type=ct, object_pk=self.post.pk, title=self.media_content.title)
        #                print u"Asocia la imagen {0} al post {1}".format(media_file, self.post.slug)
        #                m.content.save(media_file, ImageFile(open(media_file, 'r')))
        #                log.info("Imagen cargada/actualizada %s", media_file)

        #                log.info("Elimina el archivo temporal %s", media_file)
        #                try:
        #                    os.remove(media_file)
        #                except (OSError, ValueError):
        #                    log.warning("ERROR al eliminar el archivo temporal %s", media_file)
        #                    pass

        #            except IOError:
        #                log.info("IOError")
        #            
        #            except DjblogImporterException:
        #                pass

        self.post.save()
        return self.post



class DjblogImporter(object):

    app_name = 'djblog'
    model_category = 'category'
    model_post = 'post'
    model_tag = 'tag'
    model_extra = 'extracontent'

    categories = {}
    posts = {}
    extra_content = {}

    def __init__(self, fname, *args, **kwargs):
        file_data = open(fname, 'rb')
        self.file_data = json.loads(file_data.readline())

    def __iter__(self):
        for item in self.posts.iteritems():
            yield item


    def parse_category(self):
        print("Intenta migrar todas las categorías")
        # Categorias
        for obj in self.file_data:
            if obj['model'] == "{0}.{1}".format(self.app_name, self.model_category):
                cat = DjblogCategory(obj['fields']).sync()
                self.categories.update({obj['pk']: cat})
                print(obj['pk'], cat, cat.pk, obj['fields']['parent'])

        # Parents de categorias
        for obj in self.file_data:
            if obj['model'] == "{0}.{1}".format(self.app_name, self.model_category):
                if obj['fields']['parent']:
                    print(obj['pk'], obj['fields']['parent'])
                    cat =  self.categories[obj['pk']]
                    cat.parent = self.categories[obj['fields']['parent']]
                    cat.save()


    def parse_post(self):
        print("Intenta migrar todos los posts")
        for obj in self.file_data:
            if obj['model'] == "{0}.{1}".format(self.app_name, self.model_post):

                post = obj['fields']
                post['category'] = [] #[self.categories[c] for c in obj['fields']['category']]

                dp = DjblogPost(post).sync()
                dp.category.add(*[self.categories[c] for c in obj['fields']['category']])
                
                print("Migrando {0} -> {1}".format(dp.id, dp.slug))
                
                self.posts.update({obj['pk']: dp})


    def parse_extracontent(self):
        """
        Primero carga las categorías de forma temporal para luego asociar por pk
        Luego itera entre los post y los crea, luego asocia las relaciones
        """
        print("Intenta migrar todos los extra_content")
        for obj in self.file_data:
            if obj['model'] == "{0}.{1}".format(self.app_name, self.model_extra):
                post_id = obj['fields']['object_pk']
                if self.posts.get(post_id):
                    obj['fields']['object_pk'] = self.posts[post_id].pk
                    extra_content = DjblogExtraContent(obj['fields']).sync()
                    self.extra_content.update({obj['pk']: extra_content})
                    print("post_id {0} -> {1}".format(post_id, extra_content.object_pk))


    def parse_mediacontent(self, fname):

        media_data = open(fname, 'rb')
        self.media_data = json.loads(file_data.readline())


    def parse(self):
        self.parse_category()
        self.parse_post()
        self.parse_extracontent()
