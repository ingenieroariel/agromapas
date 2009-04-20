from django.conf.urls.defaults import *

# Uncomment this for admin:
from django.contrib import admin
from minagro import admin as minagroadmin
from minagro.models import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required


info_dict = {
        'queryset': Vivienda.objects.all().exclude(geometry__exact=None).order_by('departamento', 'municipio').select_related()[0:2],
#        'queryset': Vivienda.objects.all().order_by('departamento', 'municipio').select_related(),
    }
departamentos_dict = {
        'queryset': Departamento.objects.all().order_by('nombre'),
        }

urlpatterns = patterns('',
    # Example:
    # (r'^demo/', include('demo.foo.urls')),
    (r'^$', 'minagro.views.index'),
    (r'^tematico/(?P<model>\w+)/(?P<field>\w+).kmz$', 'minagro.views.tematico',)  ,
    (r'^tematico/link/(?P<model>\w+)/(?P<field>\w+).kmz$', 'django.views.generic.simple.direct_to_template', {'template': 'tematico_link.kml', 'mimetype': 'application/vnd.google-earth.kml+xml'})  ,
    (r'^select/(?P<model>\w+)/(?P<field>\w+)/(?P<value>\w+).kmz$', 'minagro.views.select',)  ,
 
    (r'^select/link/(?P<model>\w+)/(?P<field>\w+)/(?P<value>\w+).kmz$', 'django.views.generic.simple.direct_to_template', {'template': 'select_link.kml', 'mimetype': 'application/vnd.google-earth.kml+xml'})  ,
    (r'^description/(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='description.kml', mimetype="application/vnd.google-earth.kml+xml") ),
    #Debug view 
    (r'^descriptionxml/(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='description.kml', mimetype="text/xml") ),

    (r'^proyectos.(<?Pformat>kml|kmz|xml|txt)$', 'django.views.generic.list_detail.object_list',
        dict(info_dict, template_name='minagro/proyectos.kml')),
    (r'^departamentos.kmz$',
        'django.views.generic.list_detail.object_list',
        dict(departamentos_dict, template_name='minagro/departamentos.kml')),


    # Uncomment this for admin docs:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment this for admin:
    (r'^iphone/(.*)', login_required(databrowse.site.root)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    ('^admin/(.*)', admin.site.root),
)
