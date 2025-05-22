from django.db import models

from users.models import User





class Address(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)

    class Meta:
        ordering =["-id"]
