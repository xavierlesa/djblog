# -*- coding:utf-8 -*-
"""
Carga rapida y automagica de templatetags como si fueran built-in
"""

import sys
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
import logging
logger = logging.getLogger(__name__)


import django
VERSION = [i for i in django.get_version().split('.')]

if VERSION <= [1,4,5]:
    try:
        from django.template import add_to_builtins
        add_to_builtins('djblog.templatetags.getblog')
    except ImportError:
        logger.warning("Esta version de django (%s) no acepta add_to_builtins", django.get_version())
else:
    logger.warning("Esta version de django (%s) no acepta add_to_builtins, `getblog` debe cargarse a manopla", django.get_version())
