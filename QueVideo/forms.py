from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from tagulous.forms import TagField


from QueVideo.models import PlanLogistica, Artefacto, Actividad, Crudo, Recurso, ticketCalidad, comentarioTicket, Entregable

from QueVideo.serializers import RecursoSerializer


class CrudoForm(ModelForm):
    class Meta:
        model = Crudo
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ["Nombre", "Tipo", "Archivo", "etiqueta"]


class ActividadEditForm(ModelForm):
    Fecha = forms.DateTimeField()
    Video = forms.CharField(max_length=20)
    Observaciones = forms.CharField(max_length=20)
    Lugar = forms.CharField(max_length=20)

    class Meta:
        model = Actividad
        fields = ['Fecha', 'Video', 'Observaciones', 'Lugar']


class PlanLogisticaForm(ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Descripcion'})
    )

    class Meta:
        model = PlanLogistica
        fields = ['nombre', 'descripcion']


class ArtefactoRecursoForm(ModelForm):
    class Meta:
        model = Artefacto
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'Descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ['Nombre', 'Descripcion', 'Tipo', 'Archivo']


class ComentarioForm(ModelForm):
    class Meta:
        model = comentarioTicket
        widgets = {
            'Texto': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ['Texto']




class ActividadEditForm(ModelForm):
    Fecha = forms.DateTimeField()
    Video = forms.CharField(max_length=20)
    Observaciones = forms.CharField(max_length=20)
    Lugar = forms.CharField(max_length=20)

    class Meta:
        model = Actividad
        fields = ['Fecha', 'Video', 'Observaciones', 'Lugar']


class CrudoForm(ModelForm):
    class Meta:
        model = Crudo
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ["Nombre", "Tipo", "Archivo", "etiqueta"]


class ticketCalidadForm(ModelForm):
    class Meta:
        model = ticketCalidad
        widgets = {
            'Responsable': forms.Select(attrs={'class': 'form-control'}),
            'Estado': forms.Select(attrs={'class': 'form-control'}),
            'ComentarioApertura': forms.TextInput(attrs={'class': 'form-control'}),
            'Entregable': forms.Select(attrs={'class': 'form-control'}),
        }
        fields = ["Responsable", "Estado", "ComentarioApertura", "Entregable"]


class ticketSearchForm(forms.Form):
    query = forms.CharField(label='Busqueda', max_length=250)


class RecursoForm(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'recursos/crearRecurso.html'

    def get(self, request):
        recurso = get_object_or_404(Recurso)
        serializer = RecursoSerializer(recurso)
        return Response({'serializer': serializer, 'recurso': recurso})

    def post(self, request):
        recurso = get_object_or_404(Recurso)
        serializer = RecursoSerializer(recurso, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'recurso': recurso})
        serializer.save()
        return redirect('profile-list')


class entregableForm(ModelForm):
    class Meta:
        model = Entregable
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Version': forms.NumberInput(attrs={'class': 'form-control','readonly':True}),
            'ComentarioVersion': forms.TextInput(attrs={'class': 'form-control'}),
            'VideoURL': forms.URLInput(attrs={'class': 'form-control'}),
            'Recurso': forms.Select(attrs={'class': 'form-control'}),
        }
        fields = ["Nombre", "Version", "ComentarioVersion", "VideoURL","Recurso"]