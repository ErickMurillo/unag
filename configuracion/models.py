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

class Origen(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Origen de la Propiedad'

class Documento(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Documento de propiedad'

class Sistema(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Sistema de Agua'

class Animales(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Animales'

class Cultivo(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Cultivos'

class Infraestructuras(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Infraestructuras'

class DondeCotiza(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Donde cotiza'

class Cooperativa(models.Model):
    nombre = models.CharField(max_length=60)
    ubicacion = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Cooperativas'

class Proyecto(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Proyectos'

class RecibeCredito(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = '¿De quién recibe crédito?'

class FormasCredito(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Formas en que recibe crédito'

class ProblemasProductor(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Problemas más sentidos como productor'

class CambioClimatico(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Acciones cambio climático'

class AfiliacionUnag(models.Model):
    nombre = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Motivos de Afiliación'