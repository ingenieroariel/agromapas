from django import template
from django.utils.safestring import mark_safe

register = template.Library()
from django.db.models import get_model    
   
class ElevateNode(template.Node):
    def __init__(self, kml, val, max):
        base_altitude=100000
        altitude=int((val*1.0/max)*base_altitude)
        altitude=0
        self.kml= kml.replace('<Polygon>','<Polygon><extrude>0</extrude><tessellate>0</tessellate><altitudeMode>clampedToGround</altitudeMode>').replace(',0 -', ',%s -' %(altitude)).replace(',0</coordinates>',',%s</coordinates>'%(altitude))
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

''' elevate model by value(s) '''
@register.tag()
def elevate(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "elevate tag takes exactly four arguments"
    if bits[3] != 'by':
        raise TemplateSyntaxError, "third argument to elevate tag must be 'by'"
    return ElevateNode(bits[1], bits[2], bits[4])
 
@register.filter()
def currency(c):
        if c>0:
            return "$%s"%c
        else:
             return "-$%s"%(-1*c)

@register.filter()
def normalizar_valor(valor):
    return valor/100000

@register.filter()
def iconize(valor):
    return float(valor/1000000000.0)


@register.filter()
def porcentaje(valor):
    return valor*100

@register.filter()
def departamento_color(value):
    return "ccffffff"
@register.filter()
def tobgr(value):
    return '%s%s%s' % (value[4:6], value[2:4], value[0:2]) 
@register.filter()
def transparent(object):
    value=object.geometry.kml
    altitude=10000
    altitude=0
    return value.replace('<Polygon>','<Polygon id="{{object.id}}"><extrude>0</extrude><tessellate>0</tessellate><altitudeMode>clampedToGround</altitudeMode>').replace(',0 -', ',%s -' %(altitude)).replace(',0</coordinates>',',%s</coordinates>'%(altitude))

@register.filter()
def desembolsos(object):
    v1= 100*object.primer_desembolso/object.valor_total
    v2= 100*object.segundo_desembolso/object.valor_total
    v3= 100*object.tercer_desembolso/object.valor_total
    v4= 100*object.subsidio/object.valor_total
    return "%d,%d,%d,%d" % (v1,v2,v3,v4)

@register.filter()
def region_point(point):
    delta = 0.02 
    min_lod=4 
    max_lod=-1
    max_x= point.x + delta
    min_x= point.x - delta
    max_y= point.y + delta
    min_y = point.y - delta
    output='<Region><Lod><minLodPixels>%d</minLodPixels><maxLodPixels>%d</maxLodPixels></Lod><LatLonAltBox><north>%f</north><south>%f</south><east>%f</east><west>%f</west></LatLonAltBox></Region>' %(min_lod,max_lod,max_y,min_y,max_x,min_x)
    return mark_safe(output)

@register.filter()
def region_polygon(geometry):
    delta = 0.02 
    min_lod=0 
    max_lod=1024
    max_x= geometry.envelope.tuple[0][1][0]
    min_x= geometry.envelope.tuple[0][0][0]
    max_y= geometry.envelope.tuple[0][2][1]
    min_y= geometry.envelope.tuple[0][0][1]
    output='<Region><Lod><minLodPixels>%d</minLodPixels><maxLodPixels>%d</maxLodPixels></Lod><LatLonAltBox><north>%f</north><south>%f</south><east>%f</east><west>%f</west></LatLonAltBox></Region>' %(min_lod,max_lod,max_y,min_y,max_x,min_x)
    return mark_safe(output)
