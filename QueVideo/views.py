# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from django.contrib import messages

from django.urls import reverse
from ftplib import FTP

from django_tables2 import RequestConfig
from rest_framework import viewsets

from QueVideo.forms import PlanLogisticaForm, ArtefactoRecursoForm, ActividadEditForm, CrudoForm
from QueVideo.serializers import RecursoSerializer, Solicitud_CambioEstado_Serializer, EtapaSerializer
from QueVideo.tables import SolicitudesTable
from .models import PlanLogistica, Actividad, Etapa, Solicitud_CambioEstado, Crudo, Recurso
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

from django.core import serializers
from django.utils.datetime_safe import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


# ###################################################SGRED#######################################################

def index(request):
    context = {'option': 'dashboard'}
    # hard code el recurso actual para los demas requests
    # ver la documentacion de datos de sesiones en django: https://docs.djangoproject.com/en/2.1/topics/http/sessions/
    recursoActual = Recurso.objects.first()
    request.session['recurso_actual']= recursoActual.nombre
    request.session['recurso_actual_id'] = recursoActual.idRecurso
    return render(request, 'dashboard/index.html', context)


def static_tables(request):
    context = {'option': 'statictables'}
    return render(request, 'dashboard/static-tables.html', context)


def crear_Recurso(request):
    context = {'option': 'recursos'}
    return render(request, 'recursos/crearRecurso.html', context)


def ver_proyecto(request):
    context = {'option': 'proyecto'}
    return render(request, 'videos/proyecto.html', context)


def get_plan_logistica(request, planId):
    plan = PlanLogistica.objects.filter(pk=planId)

    if plan is not None:
        return HttpResponse(serializers.serialize("json", plan))
    else:
        return JsonResponse({"nombre": ''})


def get_actividades(request, planId):
    plan = PlanLogistica.objects.filter(pk=planId)
    actividades_list = Actividad.objects.filter(PlanLogistica=plan)
    return HttpResponse(serializers.serialize("json", actividades_list))


@csrf_exempt
def add_actividad(request, planId):
    plan = PlanLogistica.objects.get(pk=planId)
    if request.method == 'POST':
        print('json' + request.body)
        jact = json.loads(request.body)
        fecha = jact['fecha']
        video = jact['video']
        observaciones = jact['observaciones']
        lugar = jact['lugar']
        plan = PlanLogistica.objects.get(pk=planId)
        actividad_model = Actividad(Fecha=fecha,
                                    Video=video,
                                    Observaciones=observaciones,
                                    Lugar=lugar,
                                    PlanLogistica=plan)

        actividad_model.save()
        return JsonResponse({"ActividadId": actividad_model.pk,
                             "fecha": fecha,
                             "video": video,
                             "observaciones": observaciones,
                             "lugar": lugar})
    else:
        context = {'planLogistica': plan}
    return render(request, 'videos/addActividad.html', context)


@csrf_exempt
def edit_actividad(request, id):
    instance = get_object_or_404(Actividad, IdActividad=id)
    if request.method == 'POST':
        form = ActividadEditForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('QueVideo:proyecto'))

    else:
        # actividad = Actividad.objects.get(IdActividad=request.actividad.IdActividad)
        actividad = Actividad.objects.get(pk=id)
        actividadEditform = ActividadEditForm(instance=actividad)
        context = {"actividadEditform": actividadEditform}
    return render(request, 'videos/editActividad.html', context)


def upload_crudo(request):
    if request.method == 'POST':
        form = CrudoForm(request.POST, request.FILES)
        if form.is_valid():
            crudo = form.save()
            ftp = FTP('200.21.21.36')
            ftp.login('miso|anonymous')
            folder, name = crudo.Archivo.name.split("/")
            fileName, fileExtention = name.split(".")
            stampedName = fileName + "-" + str(crudo.IdCrudo) + "." + fileExtention
            with open(crudo.Archivo.path, 'rb') as f:
                ftp.storbinary('STOR %s' % stampedName, f)
                crudo.url = 'ftp://miso|anonymous@200.21.21.36/' + stampedName
                crudo.save()
            ftp.quit()
            if os.path.isfile(crudo.Archivo.path):
                os.remove(crudo.Archivo.path)
            messages.success(request, 'Archivo' + name + 'Guardado con Exito en el repositorio')
            return HttpResponseRedirect(reverse('QueVideo:agregarCrudo'))
    else:
        form = CrudoForm()
        crudos = Crudo.objects.all()
        return render(request, 'crudos/create.html', {'form': form, 'crudo_list': crudos})


def upload_crudo_block(request):
    if request.method == 'POST':
        form = CrudoForm(request.POST, request.FILES)
        if form.is_valid():
            crudo = form.save()
            ftp = FTP('200.21.21.36')
            ftp.login('miso|anonymous')
            folder, name = crudo.Archivo.name.split("/")
            fileName, fileExtention = name.split(".")
            stampedName = fileName + "-" + str(crudo.IdCrudo) + "." + fileExtention
            with open(crudo.Archivo.path, 'rb') as f:
                ftp.storbinary('STOR %s' % stampedName, f)
                crudo.url = 'ftp://miso|anonymous@200.21.21.36/' + stampedName
                # obtener el recurso actual desde el session manager.
                crudo.recurso = Recurso.objects.get(idRecurso = request.session['recurso_actual_id'])
                crudo.save()
            ftp.quit()
            if os.path.isfile(crudo.Archivo.path):
                os.remove(crudo.Archivo.path)
            messages.success(request, 'Archivo ' + name + ' Guardado con Exito en el repositorio de crudos del recurso: ' + request.session['recurso_actual'])
            return HttpResponseRedirect(reverse('QueVideo:agregarCrudoBlock'))
    else:
        form = CrudoForm()
        crudos = Crudo.objects.all()
        return render(request, 'crudos/createBlock.html', {'form': form, 'crudo_list': crudos})

# paso 2 kata web verde
def crudo_list(request):
    crudos = Crudo.objects.filter(recurso__idRecurso = request.session['recurso_actual_id'])
    descargados = []
    for cru in crudos:
        if request.session.get("crudo" + str(cru.IdCrudo)):
            print "crudo descargado"
            descargados.append(cru.IdCrudo)
    for x in descargados:
        print '------- for de ids de archivos descargados ------'
        print x
    return render(request, 'crudos/crudoList.html', {'crudo_list': crudos, 'descargados': descargados})


def crudo_details_download(request, crudoId):
    if request.method == 'POST':
        request.session['crudo'+ crudoId] = "descargado"
        return HttpResponseRedirect(reverse('QueVideo:crudoDownload', kwargs={'crudoId':crudoId}))
    else:
        crudo = Crudo.objects.get(pk=crudoId)
        key='crudo'+ crudoId
        status = request.session.get(key)
        return render(request, 'crudos/crudoDownload.html', {'crudo': crudo, 'status': status})


## Methods of etapa, solicitud cambio etapa CRUD

## Json class response for handle httpResponse
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


## GET  >> all list of etapa
## POST >> a new etapa

@csrf_exempt
def etapa_list(request):
    """
    List all code etapas, or create a new etapa.
    """
    if request.method == 'GET':
        etapas = Etapa.objects.all()
        serializer = EtapaSerializer(etapas, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EtapaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


## GET >> detail etapa
## PUT >> update etapa
## DELETE >> delete etapa
@csrf_exempt
def etapa_detail(request, pk):
    """
    Retrieve, update or delete a etapa.
    """
    try:
        etapa = Etapa.objects.get(idEtapa=pk)
    except Etapa.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EtapaSerializer(etapa)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EtapaSerializer(etapa, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        etapa.delete()
        return HttpResponse(status=204)


## GET  >> all list of solicitud cambio estado
## POST >> a new solicitud cambio de estado

@csrf_exempt
def solicitud_cambio_estado_list(request):
    if request.method == 'GET':
        solicitudes = Solicitud_CambioEstado.objects.all()
        serializer = Solicitud_CambioEstado_Serializer(solicitudes, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':

        nuevoEstado = json.loads(request.body)
        solicitadoPor = nuevoEstado['solicitadoPor']
        aprobadoPor = 'Sin aprobar'

        now = datetime.now()
        format_iso_now = now.isoformat()

        fecha_solicitud = format_iso_now
        fecha_aprobacion = format_iso_now

        eljson = {"solicitadoPor": solicitadoPor,
                  "aprobadoPor": aprobadoPor,
                  "fecha_solicitud": fecha_solicitud,
                  "fecha_aprobacion": fecha_aprobacion}

        serializer = Solicitud_CambioEstado_Serializer(data=eljson)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

        # solicitud_model = Solicitud_CambioEstado(
        #                             solicitadoPor=solicitadoPor,
        #                             aprobadoPor=aprobadoPor,
        #                             fecha_solicitud=fecha_solicitud,
        #                             fecha_aprobacion=fecha_aprobacion,
        #                             )
        # solicitud_model.save()
        # return JsonResponse({"solicitadoPor":solicitadoPor,
        #                         "aprobadoPor":aprobadoPor,
        #                         "fecha_solicitud":fecha_solicitud,
        #                         "fecha_aprobacion":fecha_aprobacion}, status=201)
        #
        # return HttpResponse(status=404)

        ###########
        # data = JSONParser().parse(request)


## GET >> detail solicitud cambio estado
## PUT >> update detail solicitud
## DELETE >> delete detail solicitud

@csrf_exempt
def solicitud_cambio_estado_detail(request, pk):
    try:
        solicitud = Solicitud_CambioEstado.objects.get(idSolicitud=pk)
    except Solicitud_CambioEstado.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = Solicitud_CambioEstado_Serializer(solicitud)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Solicitud_CambioEstado_Serializer(solicitud, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        solicitud.delete()
        return HttpResponse(status=204)


# ---------------------------- SGRD-19 -----------------------------
# Como  Asesor/Gestor RED debo poder ver el listado de notificaciones
# para cambio de fase del recurso para saber el avance de trabajo del recurso.


# ---------------------------- SGRD-23 -----------------------------
# Como miembro de grupo debo poder marcar la etapa
# Como miembro de grupo debo poder marcar la etapa
# como completada para solicitar avance de etapa.

# 1. Registro el cambio de Estado de etapa DONE, WAITING, PROCESS>> Registro el DONE
## DONE >> el estado actual del recurso esta completado
## WAITING >> el estado actual del recurso esta en espera de ser comenzado
## PROCESS >> el estado actual del recurso esta en desarrollo

@csrf_exempt
def cambioEstadoEtapa(request, pk):
    try:
        etapa = Etapa.objects.get(idEtapa=pk)
    except Etapa.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        nuevoEstado = json.loads(request.body)
        estado = nuevoEstado['estado']
        etapa.estado = estado
        etapa.save()
        return JsonResponse({"idEtapa": etapa.idEtapa,
                             "nombre": etapa.nombre,
                             "estado": etapa.estado,
                             "fecha_inicio": etapa.fecha_inicio,
                             "fecha_fin": etapa.fecha_fin,
                             "etapa_type": etapa.etapa_type}, status=201)
        return HttpResponse(status=404)


# ---------------------------- SGRD-18 -----------------------------
#     Como Asesor/Gestor RED debo poder realizar un avance
#     en la etapa del recurso para informar a todos los interesados
#     que la etapa actual se completa y el cambio de etapa se realiza.

# 2. Se cambia la solicitud a aprobada y se realiza el cambio de estado
# 3. Se cambia el estado de la etapa y se avanza

@csrf_exempt
def realizarAvanceEtapa(request, pk, pk2):
    try:
        etapa = Etapa.objects.get(idEtapa=pk)
        solicitud = Solicitud_CambioEstado.objects.get(idSolicitud=pk2)
    except Etapa.DoesNotExist:
        return HttpResponse(status=404)
    except Solicitud_CambioEstado.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':

        ## Cambio en la solicitud
        jbody = json.loads(request.body)
        aprobadoPor = jbody['aprobadoPor']
        solicitud.aprobadoPor = aprobadoPor
        now = datetime.now()
        format_iso_now = now.isoformat()
        solicitud.fecha_aprobacion = format_iso_now
        solicitud.save()

        ## Cambio en la etapa
        act = etapa.etapa_type
        if act == 'Pre':
            etapa.etapa_type = 'Pro'
            etapa.nombre = 'Produccion'
        elif act == 'Pro':
            etapa.etapa_type = 'Pos'
            etapa.nombre = 'Post-Produccion'
        elif act == 'Pos':
            etapa.etapa_type = 'CC'
            etapa.nombre = 'Control de calidad'
        elif act == 'CC':
            etapa.etapa_type = 'CP'
            etapa.nombre = 'Cierre de proyecto'
        elif act == 'CP':
            etapa.etapa_type = 'SR'
            etapa.nombre = 'Sistematizacion y resguardo'
        etapa.save()

        return JsonResponse({"idEtapa": etapa.idEtapa,
                             "nombre": etapa.nombre,
                             "estado": etapa.estado,
                             "fecha_inicio": etapa.fecha_inicio,
                             "fecha_fin": etapa.fecha_fin,
                             "etapa_type": etapa.etapa_type}, status=201)
        return HttpResponse(status=404)


# CONSOLE LOG CODE
# import logging, logging.config
# import sys
# LOGGING = {
#             'version': 1,
#             'handlers': {
#                 'console': {
#                     'class': 'logging.StreamHandler',
#                     'stream': sys.stdout,
#                 }
#             },
#             'root': {
#                 'handlers': ['console'],
#                 'level': 'INFO'
#             }
#         }
#
#         logging.config.dictConfig(LOGGING)
#         logging.info('' + etapa.estado)


def agregarPlanLogistica(request):
    if request.method == 'POST':
        form = PlanLogisticaForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save()
            messages.success(request, "Se Agrego el Plan de Logistica Correctamente", extra_tags="alert-success")
        return HttpResponseRedirect(reverse('QueVideo:agregarPlanLogistica'))
    else:
        form = PlanLogisticaForm(request.POST)
    return render(request, 'recursos/planLogistica.html', {'form': form})


def agregarArtefactoRecurso(request):
    if request.method == 'POST':
        form = ArtefactoRecursoForm(request.POST, request.FILES)
        if form.is_valid():
            artefacto = form.save()
            messages.success(request, "Se Agrego Insumo de Diseño Correctamente", extra_tags="alert-success")
        return HttpResponseRedirect(reverse('QueVideo:agregarInsumoRecurso'))
    else:
        form = ArtefactoRecursoForm()
    return render(request, 'recursos/insumo.html', {'form': form})


def getNotifications(request):
    table = SolicitudesTable(Solicitud_CambioEstado.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'videos/solicitudes.html', {'table': table})


# Serializadores Rest - API endpoint that allows users to be viewed or edited.

class RecursosViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all().order_by('fechaCreacion')
    serializer_class = RecursoSerializer
