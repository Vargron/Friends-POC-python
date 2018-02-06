"""friends_project URL Configuration

"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^friends/', include("apps.friend_app.urls")),
    url(r'^', include("apps.login_app.urls")),
]
