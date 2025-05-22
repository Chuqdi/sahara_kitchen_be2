from django.db import models

from categories.models import Category




class Meal(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="meals/photo")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="meals")
    is_in_stock = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    @property
    def catergoryName(self):
        return self.category.name
    
    class Meta:
        ordering = ["-id"]
    
    @property
    def created_formatted_date(self):
        return self.date_created.strftime("%b %d, %Y")