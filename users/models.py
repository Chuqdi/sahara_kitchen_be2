from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from utils.randomString import GenerateRandomString



class UserManager(BaseUserManager):
    def create(self, email, first_name, last_name, password):
        if  not email:
            raise ValueError("Please enter your  email")
        

        if  not first_name:
            raise ValueError("Please enter your first name")
        
        if  not last_name:
            raise ValueError("Please enter your last name")


        if password:
            raise ValueError("Please enter your password")

        user  = self.model(
            first_name = first_name,
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    

    def  create_super_user(self, email, full_name,phone_number, password):
        user = self.create_user(email, full_name,phone_number, password)
        user.is_active=True
        user.is_superuser=True
        user.is_staff = True
        # user.is_admin=True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(null=True, blank=True,max_length=150)
    first_name = models.CharField(null=True, blank=True,max_length=150)
    phone_number =models.CharField(unique=True,null=True, blank=True,max_length=150)
    email  = models.EmailField(blank=True, null=True, max_length=90, unique=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    referalCode = models.CharField(max_length=100, null=True, blank=True)


    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',"last_name",]



    def perm(self, *args, **kwargs):
        return True
    
    def perm_module(self, *args, **kwargs):
        return True
    

    


    def __str__(self) -> str:
        return str(self.id)







class ReferalCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referal_code")
    code = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return self.user.email



class UserEmailActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False, blank=False)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.user.email
    




def user_created(sender, instance, created, *rgs, **kwargs):
    r =ReferalCode.objects.create(user=instance, code = GenerateRandomString.randomStringGenerator(6))

    

# post_save.connect(user_created, sender=User)