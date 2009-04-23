from django.conf.urls.defaults import *

# Uncomment this for admin:
from django.contrib import admin
from minagro import admin as minagroadmin
from minagro.models import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required


departamentos_dict = {
        'queryset': Departamento.objects.all().order_by('nombre'),
        }

urlpatterns = patterns('',
    # Example:
    (r'^$', 'minagro.views.index'),
    (r'^tematico/(?P<model>\w+)/(?P<field>\w+).kmz$', 'minagro.views.tematico',)  ,
    (r'^tematico/link/(?P<model>\w+)/(?P<field>\w+).kmz$', 'django.views.generic.simple.direct_to_template', {'template': 'tematico_link.kml', 'mimetype': 'application/vnd.google-earth.kml+xml'})  ,
    (r'^select/(?P<model>\w+)/(?P<field>\w+)/(?P<value>\w+).kmz$', 'minagro.views.select',)  ,
 
    (r'^select/link/(?P<model>\w+)/(?P<field>\w+)/(?P<value>\w+).kmz$', 'django.views.generic.simple.direct_to_template', {'template': 'select_link.kml', 'mimetype': 'application/vnd.google-earth.kml+xml'})  ,

    (r'^proyectos.(?P<format>kml|kmz|txt|xml)$', 'minagro.views.object_list_kml'),

    # Uncomment this for admin docs:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment this for admin:
    (r'^iphone/(.*)', login_required(databrowse.site.root)),
	   (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'registration/login.html'} ),
    (r'^actualizar/', include('batchimport.urls')),   
    ('^admin/(.*)', admin.site.root),
)
