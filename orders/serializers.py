from meals.serializers import MealSerializer
from .models import Order, OrderQuantity
from rest_framework import serializers



class OrderQuantitySerializer(serializers.ModelSerializer):
    food = MealSerializer(many=False)
    class Meta:
        model = OrderQuantity
        fields = [
            "food",
            "quantity"
        ]


class OrderSerializer(serializers.ModelSerializer):
    quantities = OrderQuantitySerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "delivery_country",
            "delivery_first_name",
            "delivery_phone_number",
            "quantities",
            "date_ordered",
            "is_delivered",
            "is_paid",
            "delivery_address",
            "is_pay_on_delivery",
            "email",
            "checkout_id"
        ]