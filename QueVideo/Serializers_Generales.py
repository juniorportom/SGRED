from rest_framework import serializers
from .models import Etapa

class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = ('idEtapa', 'nombre', 'estado', 'fecha_inicio', 'fecha_fin','etapa_type')

class Solicitud_CambioEstado_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = ('idSolicitud', 'solicitadoPor', 'aprobadoPor', 'fecha_solicitud', 'fecha_aprobacion')
