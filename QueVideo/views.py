# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ftplib import FTP
from QueVideo.forms import PlanLogisticaForm, InsumoRecursoForm
from .models import Media, ClipForm,  EditUserForm, CustomUser, Category, EditCustomUserForm, Clip_Media, Clip, \
    PlanLogistica, Actividad, CrudoForm, Etapa, Solicitud_CambioEstado, ActividadEditForm, Crudo
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.core import serializers as jsonserializer, serializers
from django.utils.datetime_safe import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .Serializers_Generales import EtapaSerializer, Solicitud_CambioEstado_Serializer


def index(request):
    video_list = Media.objects.all()
    selected_category = 0
    selected_type = 0
    categoria_list = Category.objects.all().order_by('name')
    type_list = [{'idType': '1', 'name': 'Videos'}, {'idType': '2', 'name': 'Audios'}]

    if request.method == 'POST':
        selected_category = int(request.POST.get("idSelCategorias", 0))
        arg = request.POST.get("idSelTipo", 0)
        selected_type = int(arg)
        if selected_category != 0:
            video_list = Media.objects.filter(category=selected_category)
        if selected_type != 0:
            if selected_type == 1:
                video_list = Media.objects.filter(mediaType='V')
            else:
                if selected_type == 2:
                    video_list = Media.objects.filter(mediaType='A')

    context = {'video_list': video_list, 'categoria_list': categoria_list, 'selected_category': selected_category,
               'selected_type': selected_type, 'type_list': type_list}
    return render(request, 'videos/index.html', context)


# def login(request):
#     c = {}
#     c.update(csrf(request))
#     return render(request, 'auth/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/videos')
    else:
        return HttpResponseRedirect('/invalid')


# def loggedin(request):
#     return render_to_response('/auth/loggedin.html', {'full_name': request.user.login})


# def invalid_login(request):
#     return render(request, '/auth/invalid.html')
#
#
# def logout(request):
#     auth.logout()
#
#     return render_to_response('/auth/logout.html', )
#

def detail(request, videoid):
    if request.method == 'POST':
        form = ClipForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                clip = form.save()
                video = Media.objects.get(pk=videoid)
                current_user = request.user
                media_clip = Clip_Media(clip=clip, media=video, user=current_user)
                media_clip.save()
                mail_sender(clip.idClip)
        return HttpResponseRedirect(reverse('gallery:details', args=videoid))
    else:
        auth = 0
        if request.user.is_authenticated():
            auth = 1
        form = ClipForm()
        current_video = Media.objects.get(pk=videoid)
        context = {'video': current_video, 'form': form, 'auth': auth}
        return render(request, 'videos/details.html', context)


def detailSC(request, videoid):
    if request.method == 'POST':
        form = ClipForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                clip = form.save()
                video = Media.objects.get(pk=videoid)
                current_user = request.user
                media_clip = Clip_Media(clip=clip, media=video, user=current_user)
                media_clip.save()
        return HttpResponseRedirect(reverse('gallery:detailsSC', args=videoid))
    else:
        form = ClipForm()
        current_video = Media.objects.get(pk=videoid)
        context = {'video': current_video, 'form': form}
        return render(request, 'videos/detailsSC.html', context)


def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))


@csrf_exempt
def media_detail(request, videoid):
    video = Media.objects.filter(pk=videoid)
    return HttpResponse(jsonserializer.serialize("json", video))


def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))


@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        juser = json.loads(request.body)
        username = juser['username']
        first_name = juser['first_name']
        last_name = juser['last_name']
        password = juser['password']
        email = juser['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email

        user_app = CustomUser(pais=juser['custom']['country'],
                              ciudad=juser['custom']['city'],
                              imagen=juser['custom']['image'],
                              auth_user_id=user_model)

        user_model.save()
        user_app.save()
    return HttpResponse(serializers.serialize('json', [user_model]))


def mod_user_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        user = User.objects.get(username=request.user.username)
        customuser = CustomUser.objects.filter(auth_user_id=user).first()
        customform = EditCustomUserForm(request.POST, request.FILES, instance=customuser)

        if form.is_valid():
            if customform.is_valid():
                form.save()
                customform.save()
                return HttpResponseRedirect(reverse('gallery:index'))

    else:
        user = User.objects.get(username=request.user.username)
        print('username ' + user.username)
        form = EditUserForm(instance=user)
        customuser = CustomUser.objects.filter(auth_user_id=user).first()
        customform = EditCustomUserForm(instance=customuser)

    context = {
        'form': form,
        'customform': customform
    }

    return render(request, 'auth/modUser.html', context)


def get_user_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username,
                             "first_name": request.user.first_name,
                             "last_name": request.user.last_name,
                             "email": request.user.email})
    else:
        return JsonResponse({"username": ''})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            return HttpResponseRedirect(reverse('gallery:index'))
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'auth/changePassword.html', context)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        juser = json.loads(request.body)
        username = juser['username']
        password = juser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            mensaje = "ok"
        else:
            mensaje = "Nombre de usuario o clave no valido"
    return JsonResponse({"mensaje": mensaje})


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"mensaje": 'ok'})


@csrf_exempt
def is_logged_view(request):
    if request.user.is_authenticated:
        mensaje = 'ok'
    else:
        mensaje = 'no'
    return JsonResponse({"mensaje": mensaje})


@csrf_exempt
def ingresar(request):
    return render(request, "auth/login.html")


@csrf_exempt
def agregar_usuario(request):
    return render(request, "auth/registro.html")


def mail_sender(idClip):
    clip = Clip.objects.get(pk=idClip)
    clipmedia = Clip_Media.objects.get(clip=clip)
    media = Media.objects.get(pk=clipmedia.media.idMedia)
    send_mail(
        'Clip agregado a su video/audio',
        'Se informa que un nuevo clip ha sido agregado\n \n' +
        'Detalles\n' + 'Título del clip: ' + clip.name + '\n' + 'Video: ' + media.title + '\n\n'
        + 'Acceda a la página para poder ver el clip añadido',
        'procesosagiles201820@gmail.com',
        [media.user.email],
        fail_silently=False,
    )


# ###################################################SGRED#######################################################

def ver_proyecto(request):
    return render(request, 'videos/proyecto.html')

def get_plan_logistica(request, planId):
    plan = PlanLogistica.objects.filter(pk=planId)

    if plan is not None:
        # return JsonResponse({"nombre": plan.Nombre,
        #                      "descripcion": plan.Descripcion,
        #                      "escaleta": plan.Escaleta,
        #                      "guionTecnico": plan.GuionTecnico})
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


def agregarInsumoRecurso(request):
    if request.method == 'POST':
        form = InsumoRecursoForm(request.POST, request.FILES)
        if form.is_valid():
            insumo = form.save()
            messages.success(request, "Se Agrego Insumo de Diseño Correctamente", extra_tags="alert-success")
        return HttpResponseRedirect(reverse('QueVideo:agregarInsumoRecurso'))
    else:
        form = InsumoRecursoForm()
    return render(request, 'recursos/insumo.html', {'form': form})

from django_tables2 import RequestConfig
from .tables import SolicitudesTable

def getNotifications(request):
    table = SolicitudesTable(Solicitud_CambioEstado.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'videos/solicitudes.html', {'table': table})