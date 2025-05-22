from .views import CreateGetMeals, UpdateDeleteMeal
from django.urls import path



urlpatterns = [
    path("create_get", CreateGetMeals.as_view(), name="create_get_meals"),
    path("update_delete/<meal_id>", UpdateDeleteMeal.as_view(), name="update_delete_meals")
]
