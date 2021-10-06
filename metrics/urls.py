from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dictionnary', views.dictionnary, name='dico'),
    url(r'^browse', views.browse, name='browse'),
    url(r'^outline', views.outline, name='outline'),
]