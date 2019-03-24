from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from .models import Permissions


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]

        def save(self, commit=True):
            user = super(EditProfileForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            
            if commit:
                user.save()
            
            return user


class PermissionForm(ModelForm):
    class Meta:
        model = Permissions
        fields = [
            'permission',
        ]
