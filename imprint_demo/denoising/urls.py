from django.urls import path, re_path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    re_path(r'^(?P<factor>\d)/(?P<pid>\d+)/$', views.index, name='dnindex'),
]
