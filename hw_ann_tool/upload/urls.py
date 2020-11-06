from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    # path('review', views.review, name='review'),
    re_path(r'^review/(?P<para_id>\d+)/$', views.review, name='review'),
]