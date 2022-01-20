from typing import List

from application import path
from . import views

urlpatterns: List = [
    path('mobile', views.check_mobile),
    path("register", views.register),
    path("sms", views.sms),
]
