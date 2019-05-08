# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lugar.models import *

# Create your models here.
class Areas(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ('nombre',)

class Origen(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Origen de la Propiedad'
        ordering = ('nombre',)

class Documento(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Documento de propiedad'
        ordering = ('nombre',)

class Sistema(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Sistema de Agua'
        ordering = ('nombre',)

class Animales(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Animales'
        ordering = ('nombre',)

CHOICE_MEDIDA = (
                (1, 'Quintal'),
                (2, 'Kilogramos'),
                (3, 'Libras'),
                (4, 'Docena'),
                (5, 'Unidad'),
                )

class Cultivo(models.Model):
    nombre = models.CharField(max_length=60)
    unidad_medida = models.IntegerField(choices=CHOICE_MEDIDA,null=True,blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.nombre,self.get_unidad_medida_display())

    class Meta:
        verbose_name_plural = 'Cultivos'
        ordering = ('nombre',)

class Infraestructuras(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Infraestructuras'
        ordering = ('nombre',)

class DondeCotiza(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Donde cotiza'
        ordering = ('nombre',)

class Cooperativa(models.Model):
    nombre = models.CharField(max_length=60)
    ubicacion = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Cooperativas'
        ordering = ('nombre',)

class BancoSemilla(models.Model):
    nombre = models.CharField(max_length=60)
    ubicacion = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Bancos de Semillas'
        ordering = ('nombre',)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Proyectos'
        ordering = ('nombre',)

class RecibeCredito(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = '¿De quién recibe crédito?'
        ordering = ('nombre',)

class FormasCredito(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Formas en que recibe crédito'
        ordering = ('nombre',)

class ProblemasProductor(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Problemas más sentidos como productor'
        ordering = ('nombre',)

class CambioClimatico(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Acciones cambio climático'
        ordering = ('nombre',)

class AfiliacionUnag(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Motivos de Afiliación'
        ordering = ('nombre',)

class TipoEnergia(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Tipos de energía'
        ordering = ('nombre',)