# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from QueVideo.models import PlanLogistica, Actividad, Etapa, Recurso, Crudo, Entregable, ticketCalidad

admin.site.register(PlanLogistica)
admin.site.register(Actividad)
admin.site.register(Etapa)
admin.site.register(Recurso)
admin.site.register(Crudo)
admin.site.register(Entregable)
admin.site.register(ticketCalidad)


