"""friends_app URL Configuration

"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^add/(?P<num>[0-9]+)/$',views.add_friend),
    url(r'^remove/(?P<num>[0-9]+)/$',views.remove_friend),
    url(r'^view/(?P<num>[0-9]+)/$',views.view_friend),
    url(r'^testing123',views.test),

    url(r'^$', views.index),
]
