# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-09 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0005_auto_20181109_0939'),
        ('productores', '0009_auto_20180406_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiembroBancoSemilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(choices=[('Si', 'Si'), ('No', 'No')], max_length=2)),
                ('cooperativa', models.ManyToManyField(blank=True, to='configuracion.BancoSemilla')),
            ],
            options={
                'verbose_name_plural': '\xbfEs miembro de un Banco de Semillas?',
            },
        ),
        migrations.AlterField(
            model_name='datosfamiliares',
            name='parentesco',
            field=models.CharField(choices=[('Abuela', 'Abuela'), ('Abuelo', 'Abuelo'), ('Bisabuela', 'Bisabuela'), ('Bisabuelo', 'Bisabuelo'), ('Cu\xf1ada', 'Cu\xf1ada'), ('Cu\xf1ado', 'Cu\xf1ado'), ('Esposa', 'Esposa'), ('Esposo', 'Esposo'), ('Hermana', 'Hermana'), ('Hermano', 'Hermano'), ('Hija', 'Hija'), ('Hijo', 'Hijo'), ('Madre', 'Madre'), ('Nuera', 'Nuera'), ('Padre', 'Padre'), ('Pareja', 'Pareja'), ('Prima', 'Prima'), ('Primo', 'Primo'), ('Sobrina', 'Sobrina'), ('Sobrino', 'Sobrino'), ('Suegra', 'Suegra'), ('Suegro', 'Suegro'), ('T\xeda', 'T\xeda'), ('T\xedo', 'T\xedo'), ('Yerno', 'Yerno'), ('Nieto', 'Nieto'), ('Nieta', 'Nieta'), ('Otro', 'Otro')], max_length=200),
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='ronda',
            field=models.IntegerField(choices=[(1, 'I')]),
        ),
        migrations.AlterField(
            model_name='infraestructura',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.Infraestructuras', verbose_name='Tipo de infraestructura'),
        ),
        migrations.AlterField(
            model_name='produccionhuevosleche',
            name='tipo_produccion',
            field=models.CharField(choices=[('Producci\xf3n de huevos por mes', 'Producci\xf3n de huevos por mes'), ('Producci\xf3n de leche (litros por d\xeda)', 'Producci\xf3n de leche (litros por d\xeda)'), ('Producci\xf3n de miel (lt/a\xf1o)', 'Producci\xf3n de miel (lt/a\xf1o)'), ('Producci\xf3n de carne (kg/a\xf1o)', 'Producci\xf3n de carne (kg/a\xf1o)'), ('Producci\xf3n de pez (kg/a\xf1o)', 'Producci\xf3n de pez (kg/a\xf1o)')], max_length=40),
        ),
        migrations.AddField(
            model_name='miembrobancosemilla',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productores.Encuesta'),
        ),
    ]
