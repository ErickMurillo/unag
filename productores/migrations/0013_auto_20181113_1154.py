# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-13 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productores', '0012_auto_20181113_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='agricultura',
            name='costo_produccion',
            field=models.FloatField(blank=True, null=True, verbose_name='Costo de producci\xf3n (Inversi\xf3n) C$/Mz'),
        ),
        migrations.AddField(
            model_name='agricultura',
            name='ganancia_perdida',
            field=models.FloatField(blank=True, null=True, verbose_name='Ganancia o Perdida C$/Mz'),
        ),
        migrations.AddField(
            model_name='agricultura',
            name='ingresos_produccion',
            field=models.FloatField(blank=True, null=True, verbose_name='Ingresos de la producci\xf3n C$/Mz'),
        ),
    ]
