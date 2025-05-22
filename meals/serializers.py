from .models import Meal
from rest_framework import serializers



class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            "catergoryName",
            "id",
            "name",
            "price",
            "description",
            "photo",
            "is_in_stock",
            "category",
            "date_created",
            "created_formatted_date"
        ]
        extra_kwargs= {
            "categoryName":{
                "read_only": True
            },
            "created_formatted_date":{
                "read_only": True
            }
        }