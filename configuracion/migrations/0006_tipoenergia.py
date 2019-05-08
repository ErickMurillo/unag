# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-08 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0005_auto_20181109_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEnergia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
            ],
            options={
                'ordering': ('nombre',),
                'verbose_name_plural': 'Tipos de energ\xeda',
            },
        ),
    ]
