# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from QueVideo.models import Media, Clip, Category, Clip_Media, PlanLogistica, Actividad, Etapa

admin.site.register(Clip)
admin.site.register(Media)
admin.site.register(Category)
admin.site.register(Clip_Media)
admin.site.register(PlanLogistica)
admin.site.register(Actividad)
admin.site.register(Etapa)


