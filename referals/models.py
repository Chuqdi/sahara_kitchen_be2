from django.db import models
from django.utils import timezone
from users.models import User





class Referal(models.Model):
    refered_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name="referings")
    refering = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name="refered_by")
    is_deposited = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    recieved = models.BooleanField(default=False)


    def __str__(self):
        return self.refering.email
    

    @property
    def date_created_formatted(self):
        return self.date_created.strftime("%b %d, %Y")