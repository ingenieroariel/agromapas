from django.contrib.gis.db import models

ESTADO_CHOICES = (
            ('EJC1', 'EN EJECUCION CON 1ER. DESEMBOLSO'),
            ('EJC2', 'EN EJECUCION CON 2DO. DESEMBOLSO'),
            ('EJC3', 'EN EJECUCION CON 3ER. DESEMBOLSO'),
            ('IR', 'INTERVENIDO CON RESOLUCION'),
            ('LIQ', 'PROYECTOS LIQUIDADOS'),
            ('PI', 'POR INTERVENIR'),
            ('PLIQ', 'PROCESO DE LIQUIDACION'),
            ('RTA', 'REVISION TECNICA Y AJUSTE PARA INICION')
)

class Vivienda(models.Model):
    vigencia = models.TextField()
    acta = models.TextField() 
    radicacion = models.TextField(primary_key=True)
    departamento = models.TextField()
    municipio = models.TextField()
    localidad = models.TextField()
    tipo_solucion = models.TextField()
    hogares = models.IntegerField()
    valor_total = models.TextField()
    subsidio = models.TextField()
    desembolso1 = models.TextField() 
    fecha1 = models.DateField()
    desembolso2 = models.TextField() 
    fecha2 = models.DateField()
    desembolso3 = models.TextField() 
    fecha3 = models.DateField()
    estado = models.CharField(max_length=100, choices=ESTADO_CHOICES) 
    avance = models.DecimalField(max_digits=3, decimal_places=2)
    recursos = models.TextField()
    poblacion = models.CharField(max_length=11)
    geom = models.PointField() 

    objects = models.GeoManager()

    class Meta:
        db_table = u'vivienda'
        ordering = ['radicacion']        

    def __unicode__(self):
        return '%s, %s (%d)' % (self.localidad, self.municipio, self.vigencia)


#class Municipio(models.Model):
#    id = models.IntegerField(primary_key=True)
#    nombre = models.CharField(max_length=255, db_column='nom_mpio', null=True)
#    geometry = models.MultiPolygonField(null=True)
#
#    objects=models.GeoManager()
#
#    class Meta:
#        ordering=['nombre']
# 
#    def __unicode__(self):
#        return '%s, %s' %(self.nombre, self.id)

class Localidad(models.Model):
    cod_pob = models.TextField() 
    confiabilidad = models.DecimalField(max_digits=20, decimal_places=2)
    localidad = models.TextField()
    mpio = models.TextField()
    dpto = models.TextField()

    class Meta:  
        verbose_name_plural='localidades'

class ViviendaCode(models.Model):
    radicacion = models.TextField()
    localidad = models.TextField()
    mpio = models.TextField()
    dpto = models.TextField()

    class Meta:
        db_table = u'vivienda_code'

class Poblacion(models.Model):
    id = models.IntegerField(primary_key=True, db_column="ogc_fid")
    geometry = models.PolygonField(db_column="wkb_geometry") 
    coddane = models.TextField()
    dpto = models.TextField()
    mcpio = models.TextField()
    cpob = models.TextField()
    clase = models.TextField() 
    nom_dpto = models.TextField()
    nom_mpio = models.TextField()
    nom_cpob = models.TextField()
    tipo_clase = models.TextField()

    objects = models.GeoManager()   

    class Meta:
        db_table = u'poblaciones'
        verbose_name_plural='poblaciones'

class Departamento(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ogc_fid')
    geometry = models.PolygonField(db_column='wkb_geometry') 
    dpto = models.TextField() 
    nombre = models.TextField(db_column='nom_dpto') 
    avg_hogares = models.DecimalField(max_digits=20, decimal_places=2)
    sum_hogares = models.TextField() 
    std_hogares = models.DecimalField(max_digits=20, decimal_places=2)
    avg_avance = models.DecimalField(max_digits=20, decimal_places=2)
    sum_avance = models.TextField()
    std_avance = models.DecimalField(max_digits=20, decimal_places=2)
    avg_valor = models.DecimalField(max_digits=20, decimal_places=2)
    sum_valor = models.TextField()
    std_valor = models.DecimalField(max_digits=20, decimal_places=2)
    count = models.DecimalField(max_digits=20, decimal_places=2)
    def __unicode__(self):
        return '%s' %(self.nombre)

    objects = models.GeoManager()

    class Meta:
        db_table="departamento_vivienda"
