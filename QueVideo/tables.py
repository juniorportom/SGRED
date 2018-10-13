# tutorial/tables.py
import django_tables2 as tables
from .models import Solicitud_CambioEstado

class SolicitudesTable(tables.Table):
    class Meta:
        model = Solicitud_CambioEstado
        template_name = 'django_tables2/bootstrap.html'

