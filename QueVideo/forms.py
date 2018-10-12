from django.forms import ModelForm
from django import forms
from QueVideo.models import PlanLogistica, Insumo


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


class InsumoRecursoForm(ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Descripcion'})
    )

    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'Tipo', 'Archivo']
