from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    #url('$', views.index),
    url('input', views.newpost),
    url('output', views.output),
    url('index', views.index),
    url('info', views.info),
    url('changeH', views.changeH),
   # url('solve', views.solve),
    url(r'^solve/(?P<categ_name>\w+)/(?P<subcateg_name>\w+)/$', views.solve, name='sv1')
]
