from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('publications/', views.pub, name='pub'),
    path('partners/', views.partners, name='partners'),
    path('imgann/', views.imgann, name='imgann'),
    path('imgenh/', views.imgenh, name='imgenh'),
    path('imgsr/', views.imgsr, name='imgsr'),
    path('imgws/', views.imgws, name='imgws'),
    path('postprocess/', views.postprocess, name='postprocess'),
    re_path(r'^wr/(?P<pid>\d+)/$', views.index, name='wrindex'),
    re_path(r'^wr2/(?P<pid>\d+)/$', views.index2, name='wrindex2'),
]
