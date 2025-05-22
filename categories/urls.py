from django.urls import path
from .views import AddGetCategory, GetCategoriesWithMeal



urlpatterns = [
    path("get_with_meals", GetCategoriesWithMeal.as_view(), name="get_with_meals"),
    path("create_get",AddGetCategory.as_view(), name="create_get")
]
