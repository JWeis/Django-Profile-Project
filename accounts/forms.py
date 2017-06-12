from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms
from . import models


class CreationForm(UserCreationForm):
    class Meta:
        model = models.Profile
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio',
            'avatar'
        ]


class UpdateUserForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text="<a href=\"password/\">Update Password</a>")
    class Meta:
        model = models.Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio',
            'avatar',

        ]

    def clean_password(self):
        pass