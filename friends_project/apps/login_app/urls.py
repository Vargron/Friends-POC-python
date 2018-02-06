""" login registration app level urls
"""
from django.conf.urls import url, include
from django.contrib import admin
from .  import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$', views.login),
    url(r'^clear/$', views.clear),
    url(r'^users/$', views.view_users),
    url(r'^users/(?P<num>[0-9]+)/$',views.user_by_id),
    url(r'^users/(?P<num>[0-9]+)/edit/$', views.edit_user),
    url(r'^users/(?P<num>[0-9]+)/delete/$',views.delete_user),
    url(r'^Thor,theThundergod/$',views.create_default_admin),
    url(r'^main/$', views.main_menu),
    url(r'^logout/$', views.logout),
    url(r'^', views.index),

]
