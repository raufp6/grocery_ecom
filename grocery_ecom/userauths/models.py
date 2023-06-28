from django.db import models
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.phonenumber import PhoneNumber


class User(AbstractUser):
    username = models.EmailField(unique=True,null=True)
    # username = None 
    # username = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(unique=True,max_length=50)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name
