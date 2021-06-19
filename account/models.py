from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.

class UserData(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    token_auth = models.CharField(max_length=50, null=True, blank=True)
    user_logged_in = models.BooleanField(default=False, null=True, blank=True)
    user_verified = models.BooleanField(default=False, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


