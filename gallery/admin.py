# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from gallery.models import Media
from gallery.models import Clip
from gallery.models import Category
from gallery.models import Clip_Media

admin.site.register(Clip)
admin.site.register(Media)
admin.site.register(Category)
admin.site.register(Clip_Media)
