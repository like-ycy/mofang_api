from typing import List

from application import path
from . import views

urlpatterns: List = [
    path('mobile', views.check_mobile),
    path("register", views.register),
    path("sms", views.sms),
    path("login", views.login),
    path("info", views.info),
    path("refresh", views.refresh),
    path("verify", views.verify),
    path("logout", views.logout),
    path("avatar", views.avatar),
]
