from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    #url('$', views.index),
    url('input', views.newpost),
    url('output', views.output),
    url('index', views.index),
]
