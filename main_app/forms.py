from django import forms
from .models import Distro, Patch
from django.forms import ModelForm

class PatchForm(ModelForm):
    class Meta:
        model = Patch
        fields = '__all__'

class UploadForm(ModelForm):
    class Meta:
        model = Distro
        fields = ['name', 'photo']