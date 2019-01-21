from django.urls import path, re_path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    re_path(r'^(?P<pid>\d+)/(?P<patch_id>\d+)/$', views.index, name='hrindex'),
]
