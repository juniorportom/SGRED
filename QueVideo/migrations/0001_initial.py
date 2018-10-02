# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-23 02:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('idCategory', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('idClip', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('seg_initial', models.BigIntegerField()),
                ('seg_final', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Clip_Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Clip')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(blank=True, max_length=150)),
                ('ciudad', models.CharField(blank=True, max_length=150)),
                ('imagen', models.ImageField(blank=True, upload_to='pictures')),
                ('auth_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('idMedia', models.AutoField(primary_key=True, serialize=False)),
                ('mediaType', models.CharField(choices=[('V', 'Video'), ('A', 'Audio')], default='V', max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=255)),
                ('created', models.DateField(default=django.utils.datetime_safe.datetime.now)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=500)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Category')),
                ('clips', models.ManyToManyField(through='QueVideo.Clip_Media', to='QueVideo.Clip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clip_media',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QueVideo.Media'),
        ),
        migrations.AddField(
            model_name='clip_media',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]