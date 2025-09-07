from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # keep username (from AbstractUser)
    # make email unique as well
    email = models.EmailField(_("email address"), unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    facebook_account = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # Django will also keep first_name, last_name by default

    def __str__(self):
        return self.username
