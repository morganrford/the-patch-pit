from django.db import models
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Distro(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main_app/distros/') 
    website = models.CharField(max_length=250)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('distro_detail', kwargs={'distro_id': self.id})
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Patch(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main_app/patches/') 
    link = models.CharField(max_length=250)
    description = models.TextField(max_length=500)

    distro = models.ForeignKey(Distro, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('patch_detail', kwargs={'patch_id': self.id})
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class CustomUser(AbstractUser):
    description = models.TextField(blank=True, null=True)