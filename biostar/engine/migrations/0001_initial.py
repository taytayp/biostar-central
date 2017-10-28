# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 20:22
from __future__ import unicode_literals

import biostar.engine.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'admin'), (2, 'user')], default=2)),
                ('name', models.CharField(default='no name', max_length=256)),
                ('summary', models.TextField(default='no summary')),
                ('text', models.TextField(default='no description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('json_text', models.TextField(default='{}')),
                ('template', models.TextField(default='makefile')),
                ('uid', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default=None, upload_to=biostar.engine.models.image_path)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)),
                ('name', models.CharField(default='no name', max_length=256)),
                ('summary', models.TextField(default='no summary')),
                ('image', models.ImageField(blank=True, default=None, upload_to=biostar.engine.models.image_path)),
                ('text', models.TextField(default='no description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.IntegerField(choices=[(1, 'File'), (2, 'Collection')], default=1)),
                ('data_type', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=256, null=True)),
                ('state', models.IntegerField(choices=[(1, 'Pending'), (2, 'Ready')], default=1)),
                ('file', models.FileField(max_length=500, null=True, upload_to=biostar.engine.models.data_upload_path)),
                ('uid', models.CharField(max_length=32)),
                ('valid', models.BooleanField(default=True)),
                ('data_dir', models.FilePathField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'admin'), (2, 'user')], default=2)),
                ('name', models.CharField(default='no name', max_length=256)),
                ('summary', models.TextField(default='no summary')),
                ('image', models.ImageField(blank=True, default=None, upload_to=biostar.engine.models.image_path)),
                ('text', models.TextField(default='no description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('json_text', models.TextField(default='commands')),
                ('uid', models.CharField(max_length=32)),
                ('template', models.TextField(default='makefile')),
                ('script', models.TextField(default='')),
                ('stdout_log', models.TextField(default='', max_length=200000)),
                ('stderr_log', models.TextField(default='', max_length=200000)),
                ('valid', models.BooleanField(default=True)),
                ('state', models.IntegerField(choices=[(1, 'Queued'), (2, 'Running'), (3, 'Finished'), (4, 'Error')], default=1)),
                ('path', models.FilePathField(default='')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Analysis')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'admin'), (2, 'user')], default=2)),
                ('privacy', models.IntegerField(choices=[(3, 'Private'), (2, 'Shareable Link'), (1, 'Public')], default=2)),
                ('image', models.ImageField(blank=True, default=None, upload_to=biostar.engine.models.image_path)),
                ('name', models.CharField(default='no name', max_length=256)),
                ('summary', models.TextField(default='no summary')),
                ('text', models.TextField(default='no description', max_length=10000)),
                ('html', models.TextField(default='html')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('uid', models.CharField(max_length=32)),
                ('valid', models.BooleanField(default=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='data',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Project'),
        ),
    ]
