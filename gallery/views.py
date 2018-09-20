# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import Media, ClipForm, UserForm, EditUserForm, CustomUser, Category, EditCustomUserForm, Clip_Media, Clip

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from django.shortcuts import render_to_response

from django.contrib import auth
from django.template.context_processors import csrf

from django.core import serializers as jsonserializer, serializers


def index(request):
    video_list = Media.objects.all()
    selected_category = 0
    selected_type = 0
    categoria_list = Category.objects.all().order_by('name')
    type_list = [{'idType':'1','name':'Videos'},{'idType':'2','name':'Audios'}]

    if request.method == 'POST':
        selected_category = int(request.POST.get("idSelCategorias",0))
        arg = request.POST.get("idSelTipo",0)
        selected_type =int(arg)
        if selected_category != 0:
            video_list = Media.objects.filter(category=selected_category)
        if selected_type != 0:
            if selected_type==1:
                video_list = Media.objects.filter(mediaType='V')
            else:
                if selected_type==2:
                    video_list = Media.objects.filter(mediaType='A')

    context = {'video_list': video_list, 'categoria_list': categoria_list, 'selected_category': selected_category, 'selected_type':selected_type,'type_list':type_list}
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
        context = {'video': current_video, 'form': form, 'auth':auth}
        return render(request, 'videos/details.html', context)


def detailSC(request, videoid):
    if request.method == 'POST':
        form = ClipForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                clip = form.save()
                video = Media.objects.get(pk=videoid)
                current_user = request.user
                media_clip = Clip_Media(clip= clip, media=video, user=current_user)
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
