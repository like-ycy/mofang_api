from typing import List

from application import path
from . import views

urlpatterns: List = [
    path('mobile', views.check_mobile)
]
