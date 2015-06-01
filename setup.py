# -*- coding:utf8 -*-
#
# Copyright (c) 2014 Xavier Lesa <xavierlesa@gmail.com>.
# All rights reserved.
# Distributed under the BSD license, see LICENSE
from setuptools import setup, find_packages
import sys, os
from djblog import version

setup(name='djblog', 
        version=version, 
        description="App para crear contenido dinamico, como un blog",
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        include_package_data=True,
        install_requires=[
            'pytz',
            'Markdown',
            'django-wysiwyg-redactor',
            'requests',
        ],
        dependency_links=[
            'git+https://github.com/ninjaotoko/django-mediacontent.git',
        ],
        zip_safe=False,
        author='Xavier Lesa',
        author_email='xavierlesa@gmail.com',
        url='http://github.com/ninjaotoko/djblog'
        )
