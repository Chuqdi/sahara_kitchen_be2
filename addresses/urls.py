from django.urls import path
from .views import DeleteAddress, UpdateAddress,AddAddress

urlpatterns = [
    path("create",AddAddress.as_view(), name="add_address"),
    path("update/<id>",UpdateAddress.as_view(), name="add_address"),
    path("delete/<id>",DeleteAddress.as_view(), name="delete_address"),

]
