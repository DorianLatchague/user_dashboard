from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/new$', views.new),
    url(r'^users/edit$', views.edit_self),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/edit/(?P<id>\d+)$', views.admin_edit),
    url(r'^users/add$', views.add_user),
    url(r'^login$', views.login),
    url(r'^registering$', views.registering),
    url(r'^users/edit_info$', views.edit_info),
    url(r'^users/edit_password$', views.edit_password),
    url(r'^users/edit_desc$', views.edit_desc),
    url(r'^users/(?P<id>\d+)/admin_edit_info$', views.admin_edit_info),
    url(r'^users/(?P<id>\d+)/admin_edit_password$', views.admin_edit_password),
    url(r'^users/(?P<id>\d+)/add_message$', views.add_message),
    url(r'^users/(?P<id>\d+)/add_comment$', views.add_comment),
    url(r'^users/delete/(?P<id>\d+)$', views.delete),
    url(r'^logoff$', views.logoff),
]
