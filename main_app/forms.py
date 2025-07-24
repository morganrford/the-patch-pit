from django import forms
from .models import Distro, Patch
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class PatchForm(ModelForm):
    class Meta:
        model = Patch
        fields = '__all__'

class UploadForm(ModelForm):
    class Meta:
        model = Distro
        fields = '__all__'

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class LoginForm(forms.Form):
        username = forms.CharField(max_length=63)
        password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
     email = forms.EmailField()

     class Meta:
          model = get_user_model()
          fields = ['first_name', 'last_name', 'email', 'description']