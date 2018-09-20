# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django import forms
from django.utils.datetime_safe import datetime


class CustomUser(models.Model):
    pais = models.CharField(max_length=150, blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    imagen = models.ImageField(upload_to="pictures", blank=True)
    auth_user_id = models.ForeignKey(User, null=False)


class UserForm(ModelForm):
    usuario = forms.CharField(max_length=50)
    nombre = forms.CharField(max_length=20)
    apellido = forms.CharField(max_length=20)
    email = forms.EmailField()
    contrasena = forms.CharField(widget=forms.PasswordInput())
    contrasena2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['pais', 'ciudad', 'imagen']

    def clean_username(self):
        username = self.cleaned_data['usuario']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registrado.')
        return email

    def clean_password2(self):
        password = self.cleaned_data['contrasena']
        password2 = self.cleaned_data['contrasena']
        if password != password2:
            raise forms.ValidationError('Las claves no coinciden')
        return password2

    def __unicode__(self):
        return self.name


class EditCustomUserForm(ModelForm):
    pais = models.CharField(max_length=150, blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    imagen = models.ImageField(upload_to="pictures", blank=True)
    auth_user_id = models.ForeignKey(User, null=False)

    class Meta:
        model = CustomUser
        fields = ['pais', 'ciudad', 'imagen']


class EditUserForm(ModelForm):
    username = forms.CharField(max_length=50, disabled=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario no existe.')
        return username


class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Clip(models.Model):
    idClip = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    seg_initial = models.BigIntegerField()
    seg_final = models.BigIntegerField()


class ClipForm(ModelForm):
    class Meta:
        model = Clip
        fields = {'name', 'seg_initial', 'seg_final'}


class Clip_Media(models.Model):
    clip = models.ForeignKey('Clip')
    media = models.ForeignKey('Media')
    user = models.ForeignKey(User)


MEDIA_TYPE = (
    ('V', 'Video'),
    ('A', 'Audio'),
)


class Media(models.Model):
    idMedia = models.AutoField(primary_key=True)
    mediaType = models.CharField(max_length=255, choices=MEDIA_TYPE, default='V')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    created = models.DateField(default=datetime.now)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    clips = models.ManyToManyField(Clip, through=Clip_Media)
    category = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('details', args=[str(self.idMedia)])

    def get_absolute_SC_url(self):
        return reverse('detailsSC', args=[str(self.idMedia)])


    def get_yt_code(self):
        """Returns the ID code of a youtube video, """
        # this is specific to youtube, for other services please implement that
        # in their own function.
        # ex: https: // www.youtube.com / watch?v = wIaowvCQG1M, return wIaowvCQG1M
        if "embed" not in self.url:
            return self.url.split('?v=')[1]
        else:
            return self.url[self.url.find("embed/")+6:self.url.find("embed/")+17]

    def youTube(self):
        yt = 'https://youtube.com/embed/'
        return yt+self.get_yt_code()


    def soundCloud(self):
        return  self.url
