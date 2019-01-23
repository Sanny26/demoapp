from django.urls import path, re_path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('publications/', views.pub, name='pub'),
    path('partners/', views.partners, name='partners'),
    path('imgann/', views.imgann, name='imgann'),
    path('imgenh/', views.imgenh, name='imgenh'),
    path('imgsr/', views.imgsr, name='imgsr'),
    path('imgws/', views.imgws, name='imgws'),
    re_path(r'^(?P<pid>\d+)/$', views.index, name='wrindex'),
]
