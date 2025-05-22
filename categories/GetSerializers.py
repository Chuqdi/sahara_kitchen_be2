from rest_framework.serializers import ModelSerializer

from meals.serializers import MealSerializer
from .models import Category



class GetCategorySerializer(ModelSerializer):
    meals = MealSerializer(many=True)

    class Meta:
        model = Category
        fields = [
        "id",
        "name",
        "date_added",
        "meals"
        ]



        