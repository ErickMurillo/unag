# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
SEXO_CHOICES = (('Femenino','Femenino'), ('Masculino','Masculino'))
CELULAR_CHOICES = (('Movistar','Movistar'), ('Claro','Claro'))
SI_NO_CHOICES = (('Si','Si'), ('No','No'))
ESTADO_CIVIL_CHOICES = (('Soltero(a)','Soltero(a)'), ('Casado(a)','Casado(a)'), ('Acompañado(a)','Acompañado(a)'),
                        ('Viudo(a)','Viudo(a)'), ('Divorciado(a)','Divorciado(a)'))

class Afiliado(models.Model):
    municipio = models.ForeignKey(Municipio)
    comunidad = ChainedForeignKey(
                                Comunidad,
                                chained_field="municipio",
                                chained_model_field="municipio",
                                show_all=False, auto_choose=True)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20,verbose_name='Cédula',null=True,blank=True,unique=True)
    sexo = models.CharField(max_length=20,choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.ForeignKey(Departamento)
    anio_ingreso = models.IntegerField()
    numero_celular = models.CharField(max_length=20)
    tipo_celular = models.CharField(max_length=20,choices=CELULAR_CHOICES)
    acceso_internet = models.CharField(max_length=2,choices=SI_NO_CHOICES)
    estado_civil = models.CharField(max_length=20,choices=ESTADO_CIVIL_CHOICES)

    class Meta:
        verbose_name_plural = 'I. Datos generales del/la afiliado/a'

ESCOLARIDAD_CHOICES = (('Alfabetizado','Alfabetizado'), ('Lee y Escribe','Lee y Escribe'), ('Primaria','Primaria'),
                        ('Secundaria','Secundaria'), ('Universitario','Universitario'))

class Escolaridad(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    escolaridad = models.CharField(max_length=20,choices=ESCOLARIDAD_CHOICES)
    respuesta = models.CharField(max_length=20,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name = 'Escolaridad'

class Profesion(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    profecion = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Profesión'

PERSONAS_CHOICES = (('Adultos: Hombres','Adultos: Hombres'),('Adultos: Mujeres','Adultos: Mujeres'),
                    ('Niñas menores de 12 años','Niñas menores de 12 años'),('Niños menores de 12 años','Niños menores de 12 años'))

class PersonasDependen(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    opcion = models.CharField(max_length=25,choices=PERSONAS_CHOICES)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = 'Personas que dependen del afiliado'

class DatosFamiliares(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    nombres = models.CharField(max_length=300)
    sexo = models.CharField(max_length=20,choices=SEXO_CHOICES)
    edad =  models.IntegerField()
    escolaridad = models.CharField(max_length=300,verbose_name='Escolaridad (Último año de escolaridad)')
    parentesco = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Datos Familiares'

EMIGRAN_CHOICES = (('Local','Local'),('Nacional','Nacional'),('Centroamérica','Centroamérica'), 
                    ('Internacional','Internacional'))

TIEMPO_CHOICES = (('',''),('',''))
MESES_CHOICES = (('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),
                ('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),
                ('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),
                ('Diciembre','Diciembre'))

class FamiliaEmigra(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    hombres = models.IntegerField()
    mujeres = models.IntegerField()
    donde_emigran = models.CharField(max_length=25,choices=EMIGRAN_CHOICES)
    tiempo = models.CharField(max_length=25,choices=TIEMPO_CHOICES)
    meses = MultiSelectField(choices=MESES_CHOICES)

    class Meta:
        verbose_name_plural = 'Cuántos miembros de la familia emigran'

class Encuesta(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    fecha_encuesta = models.DateField()
    anio = models.IntegerField(editable=False)

    def __unicode__(self):
        return self.afiliado.nombre

    def save(self, *args, **kwargs):
        self.anio = self.fecha_encuesta.year
        super(Encuesta, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'II. Encuestas'

class Areas(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

class AreasFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    areas = models.ForeignKey(Areas)
    mz = models.FloatField(validators = [MinValueValidator(0.0)])

    class Meta:
        verbose_name_plural = 'Área de la Finca (Mzs)'

class OtrasTierras(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    areas = models.ForeignKey(Areas)
    mz = models.FloatField(validators = [MinValueValidator(0.0)])

    class Meta:
        verbose_name_plural = 'Otras tierras que trabaja (Mzs)'

class Origen(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Origen de la Propiedad'

class OrigenPropiedad(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    opcion = models.ForeignKey(Origen)

    class Meta:
        verbose_name_plural = 'Origen de la Propiedad'

class FormaTenencia(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    legalizada = models.CharField(max_length=2,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = 'Forma de Tenencia'

class Documento(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Documento de propiedad'

class DocumentoPropiedad(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    documento = models.ForeignKey(Documento)

    class Meta:
        verbose_name_plural = 'Documento de propiedad que posee'

class Sistema(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Sistema de Agua'

class SistemaAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    sistema = models.ManyToManyField(Sistema)

    class Meta:
        verbose_name_plural = 'Sistema de Agua Utilizado para la finca y consumo'

class EnergiaElectrica(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length=2,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '¿Tiene acceso a Energía Eléctrica?'

class Animales(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Animales'

class InventarioAnimales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    animal = models.ForeignKey(Animales)
    cantidad = models.IntegerField(validators = [MinValueValidator(0)])
    cuanto_vende = models.IntegerField(validators = [MinValueValidator(0)])

    class Meta:
        verbose_name_plural = 'Inventario de animales'

PRODUCCION_CHOICES = (('Producción de huevos por mes','Producción de huevos por mes'),
                    ('Producción de leche (litros por día)','Producción de leche (litros por día)'))

QUIEN_VENDE_CHOICES = (('Intermediarios','Intermediarios'),('Estado','Estado'),
                        ('Mercado local','Mercado local'),('Otros','Otros'))

class ProduccionHuevosLeche(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo_produccion = models.CharField(max_length=40,choices=PRODUCCION_CHOICES)
    cantidad = models.FloatField(validators = [MinValueValidator(0.0)])
    cuanto_vende = models.FloatField(validators = [MinValueValidator(0.0)])
    quien_vende = models.CharField(max_length=20,choices=QUIEN_VENDE_CHOICES)

    class Meta:
        verbose_name_plural = 'Producción de huevos y leche'

class Cultivo(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Cultivos'

CULTIVO_CHOICES = (('Cultivo de primera','Cultivo de primera'),('Cultivo de postrera','Cultivo de postrera'),
                    ('Cultivo de apante','Cultivo de apante'),('Cultivos permanentes (Frutales, Cítricos, …)','Cultivos permanentes (Frutales, Cítricos, …)'),
                    ('Otros','Otros'))

class Agricultura(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    rubro = models.ForeignKey(Cultivo)
    area_sembrada = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Área sembrada(Mz)')
    produccion_total = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Producción Total qq')
    semillas = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Semilla qq')
    consumo_humano = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Consumo humano qq')
    consumo_animal = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Consumo animal qq')
    venta = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Venta qq')
    costo_produccion = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Costo de producción (Inversión) C$/Mz')
    ingresos_produccion = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Ingresos de la producción C$/Mz')
    ganancia_perdida = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Ganancia o Perdida C$/Mz')
    tipo = models.CharField(max_length=30,choices=CULTIVO_CHOICES)

    class Meta:
        verbose_name_plural = 'Agricultura'

PRODUCCION_CHOICES = (('Intermediario','Intermediario'),('Al estado','Al estado'),
                        ('Consumidor/Mercado local','Consumidor/Mercado local'))

class VendeProduccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = MultiSelectField(choices=PRODUCCION_CHOICES)

    class Meta:
        verbose_name_plural = '¿A quién vende su producción?'


