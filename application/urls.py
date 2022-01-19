from typing import List

from application import path

urlpatterns: List = [
    path("/users", "users.urls"),
]
