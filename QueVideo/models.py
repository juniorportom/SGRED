# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django import forms
from django.utils.datetime_safe import datetime
from django.utils import timezone


class CustomUser(models.Model):
    pais = models.CharField(max_length=150, blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    imagen = models.ImageField(upload_to="pictures", blank=True)
    auth_user_id = models.ForeignKey(User, null=False)





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


class ActividadEditForm(ModelForm):
    Fecha = forms.DateTimeField()
    Video = forms.CharField(max_length=20)
    Observaciones = forms.CharField(max_length=20)
    Lugar = forms.CharField(max_length=20)
    class Meta:
        model = Actividad
        fields = ['Fecha', 'Video', 'Observaciones', 'Lugar']


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
            return self.url[self.url.find("embed/") + 6:self.url.find("embed/") + 17]

    def youTube(self):
        yt = 'https://youtube.com/embed/'
        return yt + self.get_yt_code()

    def soundCloud(self):
        return self.url


# ###################################################SGRED#######################################################
CRUDO_TYPE = (
    ('V', 'Video'),
)


class Crudo(models.Model):
    IdCrudo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=150, blank=False, unique=True)
    Tipo = models.CharField(max_length=50, choices=CRUDO_TYPE, default='V', blank=False)
    Archivo = models.FileField(upload_to='crudos', null=True)
    url = models.CharField(max_length=2000, blank=False, default=" ")


class CrudoForm(ModelForm):
    class Meta:
        model = Crudo
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        fields = ["Nombre", "Tipo", "Archivo"]


# ---------------------------- SGRD-18-----------------------------
#     Como Asesor/Gestor RED debo poder realizar un avance
#     en la etapa del recurso para informar a todos los interesados
#     que la etapa actual se completa y el cambio de etapa se realiza.

# ---------------------------- SGRD-19-----------------------------
#   Como  Asesor/Gestor RED debo poder ver el listado de notificaciones
#   para cambio de fase del recurso para saber el avance de trabajo del recurso.

# class Recurso(models.Model):
#     etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
#     solicitud_cambio = models.ForeignKey(Solicitud_CambioEstado, on_delete=models.CASCADE)
#     idRecurso = models.AutoField(primary_key=True)
#     nombre  = models.CharField(max_length=255)
#     estado  = models.CharField(max_length=255, choices=ESTADO_TYPE)
#     def __unicode__(self):
#         return self.nombre


class Etapa(models.Model):
    ETAPA_TYPE = (
        ('Pre', 'Pre-Produccion'),
        ('Pro', 'Produccion'),
        ('Pos', 'Post-Produccion'),
        ('CC', 'Control de calidad'),
        ('CP', 'Cierre de proyecto'),
        ('SR', 'Sistematizacion y resguardo'),
    )

    ESTADO_TYPE = (
        ('WAITING', 'Pendiente'),
        ('PROCESS', 'En Proceso'),
        ('DONE', 'Terminado'),
    )

    idEtapa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    estado = models.CharField(max_length=255, choices=ESTADO_TYPE)
    fecha_inicio = models.DateTimeField(default=datetime.now)
    fecha_fin = models.DateTimeField('fecha de finalizacion no definida')
    etapa_type = models.CharField(max_length=255, choices=ETAPA_TYPE)

    def __unicode__(self):
        return self.nombre


class Solicitud_CambioEstado(models.Model):
    idSolicitud = models.AutoField(primary_key=True)
    solicitadoPor = models.CharField(max_length=255)
    aprobadoPor = models.CharField(max_length=255, default='No se ha aprobado')
    fecha_solicitud = models.DateTimeField(default=datetime.now)
    fecha_aprobacion = models.DateTimeField('fecha de aprobacion no definida')

    def __unicode__(self):
        return self.nombre

    def was_requested_recently(self):
        return self.fecha_solicitud >= timezone.now() - datetime.timedelta(days=1)


TIPO_INSUMO = (
    ('E', 'Escaleta'),
    ('SB', 'StoryBoard'),
    ('GT', 'Guion Tecnico'),
    ('REU', 'Reunion'),
    ('REF', 'Referente'),
)

class Insumo(models.Model):
    IdInsumo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Descripcion = models.CharField(max_length=255)
    Tipo = models.CharField(max_length=255, choices=TIPO_INSUMO, default='E')
    Archivo = models.FileField(upload_to='insumos/', null=True)

class ArchivoInsumo(models.Model):
    IdArchivo = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Ubicacion = models.CharField(max_length=255)
    valor = models.CharField(max_length=64)