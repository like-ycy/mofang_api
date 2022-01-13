from typing import List

from application import path
from . import views

urlpatterns: List = [
    path("/home", views.index, methods=['GET']),
]
