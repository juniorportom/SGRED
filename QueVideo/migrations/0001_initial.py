# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-03 08:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('IdActividad', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha', models.DateTimeField()),
                ('Video', models.CharField(max_length=64)),
                ('Observaciones', models.CharField(max_length=255)),
                ('Lugar', models.CharField(max_length=255)),
                ('Estado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArchivoArtefacto',
            fields=[
                ('IdArchivo', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=64)),
                ('Ubicacion', models.CharField(max_length=255)),
                ('valor', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Artefacto',
            fields=[
                ('IdArtefacto', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=64)),
                ('Descripcion', models.CharField(max_length=255)),
                ('Tipo', models.CharField(choices=[('E', 'Escaleta'), ('SB', 'StoryBoard'), ('GT', 'Guion Tecnico'), ('REU', 'Reunion'), ('REF', 'Referente')], default='E', max_length=255)),
                ('Archivo', models.FileField(null=True, upload_to='artefacto/')),
            ],
        ),
        migrations.CreateModel(
            name='Crudo',
            fields=[
                ('IdCrudo', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=150, unique=True)),
                ('Tipo', models.CharField(choices=[('V', 'Video')], default='V', max_length=50)),
                ('Archivo', models.FileField(null=True, upload_to='crudos')),
                ('url', models.CharField(default=' ', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('idEtapa', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('WAITING', 'Pendiente'), ('PROCESS', 'En Proceso'), ('DONE', 'Terminado')], max_length=255)),
                ('fecha_inicio', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True, verbose_name='fecha de finalizacion no definida')),
                ('etapa_type', models.CharField(choices=[('Pre', 'Pre-Produccion'), ('Pro', 'Produccion'), ('Pos', 'Post-Produccion'), ('CC', 'Control de calidad'), ('CP', 'Cierre de proyecto'), ('SR', 'Sistematizacion y resguardo')], max_length=255)),
                ('siguiente_etapa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Etapa')),
            ],
        ),
        migrations.CreateModel(
            name='PlanLogistica',
            fields=[
                ('IdPlanLogistica', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=64)),
                ('Descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('idRecurso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(default='', max_length=255)),
                ('estado', models.CharField(choices=[('WAITING', 'Pendiente'), ('PROCESS', 'En Proceso'), ('DONE', 'Terminado')], max_length=255)),
                ('proyecto', models.CharField(max_length=255)),
                ('fechaCreacion', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('Tipo', models.CharField(choices=[('VD', 'VIDEO')], default='VD', max_length=255)),
                ('etapa', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Etapa')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud_CambioEstado',
            fields=[
                ('idSolicitud', models.AutoField(primary_key=True, serialize=False)),
                ('solicitadoPor', models.CharField(max_length=255)),
                ('aprobadoPor', models.CharField(default='No se ha aprobado', max_length=255)),
                ('fecha_solicitud', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('fecha_aprobacion', models.DateTimeField(verbose_name='fecha de aprobacion no definida')),
            ],
        ),
        migrations.CreateModel(
            name='Tagulous_Crudo_etiqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='tagulous_crudo_etiqueta',
            unique_together=set([('slug',)]),
        ),
        migrations.AddField(
            model_name='recurso',
            name='solicitud_cambio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Solicitud_CambioEstado'),
        ),
        migrations.AddField(
            model_name='recurso',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='crudo',
            name='etiqueta',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, help_text='Enter a comma-separated tag string', to='QueVideo.Tagulous_Crudo_etiqueta'),
        ),
        migrations.AddField(
            model_name='crudo',
            name='recurso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Recurso'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='PlanLogistica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QueVideo.PlanLogistica'),
        ),
    ]
