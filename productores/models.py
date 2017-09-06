# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lugar.models import *
from configuracion.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from sorl.thumbnail import ImageField
import datetime
from django.contrib.auth.models import User

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
    lugar_nacimiento = models.CharField(max_length=250)
    foto = ImageField(upload_to='productores/',blank=True, null=True)
    anio_ingreso = models.IntegerField(verbose_name='Año ingreso',blank=True, null=True)
    numero_celular = models.CharField(max_length=20,blank=True, null=True)
    tipo_celular = models.CharField(max_length=20,choices=CELULAR_CHOICES,blank=True, null=True)
    edad = models.IntegerField(editable=False)

    class Meta:
        verbose_name_plural = 'I. Datos generales del/la afiliado/a'

    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        #calcular edad a partir de fecha nacimiento
        today = datetime.date.today()
        self.edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        super(Afiliado, self).save(*args, **kwargs)

class Encuesta(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    fecha_encuesta = models.DateField()
    anio = models.IntegerField(editable=False)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.afiliado.nombre

    def save(self, *args, **kwargs):
        self.anio = self.fecha_encuesta.year
        super(Encuesta, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'II. Encuestas'

class DatosGenerales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    acceso_internet = models.CharField(max_length=2,choices=SI_NO_CHOICES,blank=True, null=True)
    estado_civil = models.CharField(max_length=20,choices=ESTADO_CIVIL_CHOICES)
    # edad = models.IntegerField(editable=False)

    class Meta:
        verbose_name_plural = 'Datos generales'

ESCOLARIDAD_CHOICES = (('Primaria','Primaria'),
                        ('Secundaria','Secundaria'), ('Universitario','Universitario'))

class Escolaridad(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    escolaridad = models.CharField(max_length=20,choices=SI_NO_CHOICES, verbose_name='Lee y escribe')
    nivel_escolaridad = models.CharField(max_length=20,choices=ESCOLARIDAD_CHOICES)
    # respuesta = models.CharField(max_length=20,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = 'Escolaridad afiliado'

class Profesion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    profecion = models.CharField(max_length=200,verbose_name='Profesión')

    class Meta:
        verbose_name_plural = 'Profesión'

PERSONAS_CHOICES = (('Adultos: Hombres','Adultos: Hombres'),('Adultos: Mujeres','Adultos: Mujeres'),
                    ('Niñas menores de 12 años','Niñas menores de 12 años'),('Niños menores de 12 años','Niños menores de 12 años'))

class PersonasDependen(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    opcion = models.CharField(max_length=25,choices=PERSONAS_CHOICES)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Personas que dependen del afiliado'

EMIGRAN_CHOICES = (('Local','Local'),('Nacional','Nacional'),('Centroamérica','Centroamérica'), 
                    ('Internacional','Internacional'))

TIEMPO_CHOICES = (('< 1 mes','< 1 mes'),('1-3 meses','1-3 meses'),('4-6 meses','4-6 meses'),
                    ('7-12 meses','7-12 meses'),('> 12 meses','> 12 meses'))

MESES_CHOICES = (('Enero','Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),
                ('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),
                ('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),
                ('Diciembre','Diciembre'))

class DatosFamiliares(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    nombres = models.CharField(max_length=300)
    sexo = models.CharField(max_length=20,choices=SEXO_CHOICES)
    fecha_nacimiento =  models.DateField()
    escolaridad = models.CharField(max_length=300,verbose_name='Escolaridad (Último año de escolaridad)',choices=ESCOLARIDAD_CHOICES)
    parentesco = models.CharField(max_length=200)
    donde_emigran = models.CharField(max_length=25,choices=EMIGRAN_CHOICES,blank=True,null=True)
    tiempo = models.CharField(max_length=25,choices=TIEMPO_CHOICES,blank=True,null=True)
    meses = MultiSelectField(choices=MESES_CHOICES,blank=True)
    edad = models.IntegerField(editable=False)

    class Meta:
        verbose_name_plural = 'Datos Familiares'

    def save(self, *args, **kwargs):
        #calcular edad a partir de fecha nacimiento
        today = datetime.date.today()
        self.edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        super(DatosFamiliares, self).save(*args, **kwargs)

class FamiliaEmigra(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    hombres = models.IntegerField()
    mujeres = models.IntegerField()
    donde_emigran = models.CharField(max_length=25,choices=EMIGRAN_CHOICES)
    tiempo = models.CharField(max_length=25,choices=TIEMPO_CHOICES)
    meses = MultiSelectField(choices=MESES_CHOICES)

    class Meta:
        verbose_name_plural = 'Cuántos miembros de la familia emigran'

class AreasFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    areas = models.ForeignKey(Areas)
    mz = models.FloatField(validators = [MinValueValidator(0.0)])
    origen = models.ForeignKey(Origen)

    class Meta:
        verbose_name_plural = 'Área de la Finca (Mzs)'

class TierrasAlquiladas(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    posse = models.CharField(max_length=20,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = 'Posse tierras alquiladas'

class OtrasTierras(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    areas = models.ForeignKey(Areas)
    mz = models.FloatField(validators = [MinValueValidator(0.0)])

    class Meta:
        verbose_name_plural = 'Otras tierras que trabaja (Mzs)'

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

class DocumentoPropiedad(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    documento = models.ForeignKey(Documento)

    class Meta:
        verbose_name_plural = 'Documento de propiedad que posee'

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

CULTIVO_CHOICES = (('Cultivo de primera','Cultivo de primera'),('Cultivo de postrera','Cultivo de postrera'),
                    ('Cultivo de apante','Cultivo de apante'),('Cultivos permanentes (Frutales, Cítricos, …)','Cultivos permanentes (Frutales, Cítricos, …)'),
                    ('Otros','Otros'))

PRODUCCION_CHOICES2 = (('Intermediario','Intermediario'),('Al estado','Al estado'),
                        ('Consumidor / Mercado local','Consumidor / Mercado local'),
                        ('Mercado nacional','Mercado nacional'),('Mercado internacional / Exportación','Mercado internacional / Exportación'))

class Agricultura(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    rubro = models.ForeignKey(Cultivo)
    area_sembrada = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Área sembrada(Mz)')
    produccion_total = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Producción Total qq')
    semillas = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Semilla qq')
    consumo_humano = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Consumo humano qq')
    consumo_animal = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Consumo animal qq')
    venta = models.FloatField(validators = [MinValueValidator(0.0)],verbose_name='Venta qq')
    quien_vende = models.CharField(max_length=50,choices=PRODUCCION_CHOICES2)
    costo_produccion = models.FloatField(verbose_name='Costo de producción (Inversión) C$/Mz')
    ingresos_produccion = models.FloatField(verbose_name='Ingresos de la producción C$/Mz')
    ganancia_perdida = models.FloatField(verbose_name='Ganancia o Perdida C$/Mz')
    tipo = models.CharField(max_length=30,choices=CULTIVO_CHOICES)

    class Meta:
        verbose_name_plural = 'Agricultura'

class VendeProduccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = MultiSelectField(choices=PRODUCCION_CHOICES2)

    class Meta:
        verbose_name_plural = '¿A quién vende su producción?'


class ManoObra(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    mano_obra = models.CharField(max_length=2,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '¿Contrata mano de obra?'

class TablaEmpleo(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    rubro = models.ForeignKey(Cultivo)
    temporal_hombres = models.IntegerField(validators = [MinValueValidator(0)])
    temporal_mujeres = models.IntegerField(validators = [MinValueValidator(0)])
    permanente_hombres = models.IntegerField(validators = [MinValueValidator(0)])
    permanente_mujeres = models.IntegerField(validators = [MinValueValidator(0)])
    familiar_hombres = models.IntegerField(validators = [MinValueValidator(0)])
    familiar_mujeres = models.IntegerField(validators = [MinValueValidator(0)])

    class Meta:
        verbose_name_plural = 'Empleo'

class Infraestructura(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo = models.ForeignKey(Infraestructuras)
    # possee = models.CharField(max_length=2,choices=SI_NO_CHOICES)

class Cotizacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length=2,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '¿Cotiza?'

DESDE_CUANDO_CHOICES = (('Menor 1 año','Menor 1 año'),('Mas de 1 año','Mas de 1 año'))

FRECUENCIA_CHOICES = (('Mensual','Mensual'),('Trimestral','Trimestral'),
                        ('Semestral','Semestral'),('Anual','Anual'))

class RespuestaSiCotiza(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    donde_cotiza = models.ForeignKey(DondeCotiza)
    desde_cuando = models.CharField(max_length=25,choices=DESDE_CUANDO_CHOICES)
    cuanto_cotiza = models.FloatField(validators = [MinValueValidator(0.0)])
    frecuencia = models.CharField(max_length=25,choices=FRECUENCIA_CHOICES)

    class Meta:
        verbose_name_plural = 'Si la respuesta es SI'

class MiembroCooperativa(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length=2,choices=SI_NO_CHOICES)
    cooperativa = models.ManyToManyField(Cooperativa,blank=True)

    class Meta:
        verbose_name_plural = '¿Es miembro de Cooperativa?'

class BeneficiadoProyecto(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length=2,choices=SI_NO_CHOICES)
    proyectos = models.ManyToManyField(Proyecto,blank=True)

    class Meta:
        verbose_name_plural = '¿Es beneficiado por otros proyectos o programa del gobierno?'

class Credito(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length=2,choices=SI_NO_CHOICES)
    proyectos = models.ForeignKey(RecibeCredito,blank=True,null=True,verbose_name='De quien recibe el credito')
    formas_recibe_credito = models.ManyToManyField(FormasCredito,blank=True)

    class Meta:
        verbose_name_plural = '¿Recibe crédito?'

class CotizacionOrganizacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    problemas_productor = models.ManyToManyField(ProblemasProductor,verbose_name='Problemas más sentidos como productor',blank=True)
    acciones_cambio_climatico = models.ManyToManyField(CambioClimatico,verbose_name='Acciones que realiza para enfrentar el cambio climático',blank=True)
    afiliacion_unag = models.ManyToManyField(AfiliacionUnag,verbose_name='Motivos de Afiliación a la UNAG',blank=True)
    comentarios = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name='Cotización y Organización'