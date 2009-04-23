# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.db.models import get_model
from django.utils.safestring import mark_safe
from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
from django.shortcuts import render_to_response
from minagro.models import Vivienda

def index(request):
    return render_to_response('index.html', {"GMAPS_API_KEY": settings.GMAPS_API_KEY}, context_instance=RequestContext(request))
def set_colores(object_list, field):
    color_set=['000080', 'ff0000', '9400d3', '008b00', 'eeee00', '0a0a0a', 'a9d2c4', '61ccb0', 'a7b6f9']
    objects={}
    colores_level={
            '1': color_set[0],
            '2': color_set[1],
            '3': color_set[2],
            '4': color_set[3],
            '5': color_set[4],  
            }
    for object in object_list:
        id_str='%d' % (object.id)
        color= 'FFFFFF'
        colores=None
        levels=5
        mayor=object_list.order_by('-%s' % (field))[0].__getattribute__(field)
        valor=object.__getattribute__(field)
        level=int((valor*1.0/mayor)*levels+1)
        if level > levels:
            level=levels
        level_key='%s' % (level)
        color=colores_level[level_key]
        colores=[ ]
        for level in range(levels):
            valor1='%s' % (mayor/(level+1))
            color1=colores_level['%s' % (level+1)]
            colores.append({'valor': valor1, 'color':color1 })
        objects[id_str]=color
    return objects, colores

def tematico(request, model, field):
    object_model = get_model('minagro', model)
    object_list=object_model.objects.all()
    point=polygon=False
    objects, colores =set_colores(object_list, field)
    top={}
    if object_list[0].geometry.num_points== 1:
        point = True
        for o in object_list.order_by('-%s' %(field))[0:5]:
           top[o.localidad]=o.geometry.kml # Reemplazar localidad por un campo generico.
    else:
        polygon=True
        for o in object_list.order_by('-%s' %(field))[0:5]:
            top[o.nombre]=mark_safe(o.geometry.centroid.kml)

    return render_to_response('tematico.kml', {'objects':objects, 'colores':colores,'model':model, 'field':field, 'point':point, 'polygon': polygon, 'top':top} ,context_instance=RequestContext(request), )

def select(request, model, field, value):

    object_model = get_model('minagro', model)
    object_list=object_model.objects.all()
    if value == 'all':
        objects_visible=object_list
        objects_invisible=object_list.none()
    elif value == 'none':
        objects_visible=object_list.none()
        objects_invisible=object_list
    else:
        objects_visible=object_model.objects.extra(where=['%s = \'%s\'' % (field, value)])
        objects_invisible=object_model.objects.extra(where=['%s != \'%s\'' % (field, value)])  
    objects={}
    for object in objects_visible:
        objects['%s' % (object.id)]='1'
    for object in objects_invisible:
        objects['%s' % (object.id)]='0'
        
    return render_to_response('select.kml', {'objects':objects,'objects_visible':objects_visible, 'model':model, 'field':field, 'value':value} ,context_instance=RequestContext(request), )

def object_list_kml(request, format='kml', template_name="minagro/proyectos.kml"):
    viviendas= Vivienda.objects.all().exclude(geometry__exact=None).order_by('departamento', 'municipio').select_related()
    if format == 'kml':
        return render_to_kml(template_name, {'object_list':viviendas})
    if format == 'kmz':
        return render_to_kmz(template_name, {'object_list':viviendas})
    if format == 'xml':
        return render_to_response(template_name, {'object_list':viviendas}, mimetype="text/xml")
    if format == 'txt':
        return render_to_response(template_name, {'object_list':viviendas}, mimetype="text/plain")
