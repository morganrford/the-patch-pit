from django.db import models
from django.urls import reverse

class Distro(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main_app/distros/', null=True, blank=True) 
    website = models.CharField(max_length=250)
    description = models.TextField(max_length=500)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('distro_detail', kwargs={'distro_id': self.id})
    
class Patch(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main_app/patches/', null=True, blank=True) 
    link = models.CharField(max_length=250)
    description = models.TextField(max_length=500)

    distro = models.ForeignKey(Distro, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('patch_detail', kwargs={'patch_id': self.id})