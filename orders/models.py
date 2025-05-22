from django.db import models
from meals.models import Meal

from users.models import User

class OrderQuantity(models.Model):
    food = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=300)
    delivery_country = models.TextField()
    delivery_first_name = models.TextField()
    delivery_last_name = models.TextField()
    delivery_address = models.TextField(null=True, blank=True)
    delivery_phone_number = models.TextField()
    quantities = models.ManyToManyField(OrderQuantity,)
    date_ordered=models.DateField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_pay_on_delivery = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.email

