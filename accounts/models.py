from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator


class Profile(User, models.Model):
    username_validator = ASCIIUsernameValidator()
    date_of_birth = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(blank=True, upload_to='static/extra_credit_image_editor')

    class Meta:
        pass

    def __str__(self):
        return self.username
