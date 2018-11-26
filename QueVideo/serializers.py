from rest_framework import serializers

from QueVideo.models import Recurso, Etapa, Solicitud_CambioEstado, Entregable


class RecursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recurso
        fields = ('idRecurso', 'nombre', 'Tipo','descripcion')


class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = ('idEtapa', 'nombre', 'estado', 'fecha_inicio', 'fecha_fin','etapa_type')


class Solicitud_CambioEstado_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud_CambioEstado
        fields = ('idSolicitud', 'solicitadoPor', 'aprobadoPor', 'fecha_solicitud', 'fecha_aprobacion')

class EntregableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entregable
        fields = ('IdEntregable', 'Nombre', 'Version', 'ComentarioVersion', 'VideoURL','FechaModificacion','Recurso')
