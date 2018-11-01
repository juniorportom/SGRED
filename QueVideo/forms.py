from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from QueVideo.models import PlanLogistica, Artefacto, Actividad, Crudo, Recurso
from QueVideo.serializers import RecursoSerializer


class CrudoForm(ModelForm):
    class Meta:
        model = Crudo
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Archivo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        fields = ["Nombre", "Tipo", "Archivo"]


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
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Descripcion'})
    )

    class Meta:
        model = Artefacto
        fields = ['nombre', 'descripcion', 'Tipo', 'Archivo']


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
        }
        fields = ["Nombre", "Tipo", "Archivo"]



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
