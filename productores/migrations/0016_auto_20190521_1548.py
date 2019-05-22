# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-21 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0007_productosprocesados'),
        ('productores', '0015_procesamiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuentesAguaFinca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta')),
                ('fuentes', models.ManyToManyField(to='configuracion.Sistema')),
            ],
            options={
                'verbose_name_plural': 'Fuentes de agua en la finca',
            },
        ),
        migrations.AlterModelOptions(
            name='sistemaagua',
            options={'verbose_name_plural': 'Sistema de Agua Utilizado para el consumo en el hogar'},
        ),
        migrations.AlterField(
            model_name='produccionhuevosleche',
            name='tipo_produccion',
            field=models.CharField(choices=[('Producci\xf3n de leche (litros por d\xeda)', 'Leche (litros por d\xeda)'), ('Producci\xf3n de carne (kg/a\xf1o)', 'Carne de res (lbs/a\xf1o)'), ('Producci\xf3n de huevos por mes', 'Huevos (und/mes)'), ('Carne Av\xedcola (lbs/mes)', 'Carne Av\xedcola (lbs/mes)'), ('Carne de cerdo (lbs/a\xf1o)', 'Carne de cerdo (lbs/a\xf1o)'), ('Carne de pelibuey lbs/a\xf1o', 'Carne de pelibuey lbs/a\xf1o'), ('Leche de cabra (litros/d\xeda)', 'Leche de cabra (litros/d\xeda)'), ('Producci\xf3n de miel (lt/a\xf1o)', 'Miel (lt/a\xf1o)'), ('Producci\xf3n de pez (kg/a\xf1o)', 'Pez (kg/a\xf1o)')], max_length=40),
        ),
    ]