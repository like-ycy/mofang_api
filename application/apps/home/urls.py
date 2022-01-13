from typing import List

from application import path
from . import views

urlpatterns: List = [
    path("/index", views.index, methods=['GET']),
    path("/test", views.test, methods=['GET']),
]
