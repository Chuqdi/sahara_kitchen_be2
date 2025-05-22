from django.db import models




class Category(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name