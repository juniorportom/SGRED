# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils import timezone
import tagulous.models
from django.contrib.auth.models import User

# ################################################### ---- SGRED ----- #######################################################


class PlanLogistica(models.Model):
    IdPlanLogistica = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Descripcion = models.CharField(max_length=255)


class Actividad(models.Model):
    IdActividad = models.AutoField(primary_key=True)
    Fecha = models.DateTimeField()
    Video = models.CharField(max_length=64)
    Observaciones = models.CharField(max_length=255)
    Lugar = models.CharField(max_length=255)
    PlanLogistica = models.ForeignKey(PlanLogistica)
    Estado= models.BooleanField(default=False)

    # ---------------------------- SGRD-18-----------------------------
    #     Como Asesor/Gestor RED debo poder realizar un avance
    #     en la etapa del recurso para informar a todos los interesados
    #     que la etapa actual se completa y el cambio de etapa se realiza.

    # ---------------------------- SGRD-19-----------------------------
    #   Como  Asesor/Gestor RED debo poder ver el listado de notificaciones
    #   para cambio de fase del recurso para saber el avance de trabajo del recurso.


ESTADO_TYPE = (
    ('WAITING', 'Pendiente'),
    ('PROCESS', 'En Proceso'),
    ('DONE', 'Terminado'),
)

ETAPA_TYPE = (
    ('Pre', 'Pre-Produccion'),
    ('Pro', 'Produccion'),
    ('Pos', 'Post-Produccion'),
    ('CC', 'Control de calidad'),
    ('CP', 'Cierre de proyecto'),
    ('SR', 'Sistematizacion y resguardo'),
)


class Etapa(models.Model):
    idEtapa = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=255, choices=ESTADO_TYPE)
    fecha_inicio = models.DateTimeField(default=datetime.now)
    fecha_fin = models.DateTimeField('fecha de finalizacion no definida', blank=True, null=True)
    etapa_type = models.CharField(max_length=255, choices=ETAPA_TYPE)

    def __unicode__(self):
        return str(self.idEtapa)


TIPO_RECURSO = (
    ('VD', 'VIDEO'),

)


class Solicitud_CambioEstado(models.Model):
    idSolicitud = models.AutoField(primary_key=True)
    solicitadoPor = models.CharField(max_length=255)
    aprobadoPor = models.CharField(max_length=255, default='No se ha aprobado')
    fecha_solicitud = models.DateTimeField(default=datetime.now)
    fecha_aprobacion = models.DateTimeField('fecha de aprobacion no definida')

    def was_requested_recently(self):
        return self.fecha_solicitud >= timezone.now() - datetime.timedelta(days=1)


# Recurso

class Recurso(models.Model):
    idRecurso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255,default='')
    estado = models.CharField(max_length=255, choices=ESTADO_TYPE)
    proyecto = models.CharField(max_length=255)
    fechaCreacion = models.DateTimeField(default=datetime.now)
    etapa = models.CharField(max_length=255, choices=ETAPA_TYPE)

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    etapa_history = models.ForeignKey(Etapa, on_delete=models.CASCADE, blank=True, null=True)
    solicitud_cambio = models.ForeignKey(Solicitud_CambioEstado, on_delete=models.CASCADE, blank=True, null=True)
    Tipo = models.CharField(max_length=255, choices=TIPO_RECURSO, default='VD')

    def __unicode__(self):
        return self.nombre

CRUDO_TYPE = (
    ('V', 'Video'),
)


class Crudo(models.Model):
    IdCrudo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=150, blank=False, unique=True)
    Tipo = models.CharField(max_length=50, choices=CRUDO_TYPE, default='V', blank=False)
    Archivo = models.FileField(upload_to='crudos', null=True)
    url = models.CharField(max_length=2000, blank=False, default=" ")
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, default=1)
    etiqueta = tagulous.models.TagField()

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('QueVideo:crudoDownload', args=[str(self.IdCrudo)])


TIPO_ARTEFACTO = (
    ('E', 'Escaleta'),
    ('SB', 'StoryBoard'),
    ('GT', 'Guion Tecnico'),
    ('REU', 'Reunion'),
    ('REF', 'Referente'),
)


class Artefacto(models.Model):
    IdArtefacto = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Descripcion = models.CharField(max_length=255)
    Tipo = models.CharField(max_length=255, choices=TIPO_ARTEFACTO, default='E')
    Archivo = models.FileField(upload_to='artefacto/', null=True)


class ArchivoArtefacto(models.Model):
    IdArchivo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Ubicacion = models.CharField(max_length=255)
    valor = models.CharField(max_length=64)
