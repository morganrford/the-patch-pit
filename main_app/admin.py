from django.contrib import admin
from .models import Distro, Patch
from django.contrib.auth import get_user_model

class DistroAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Distro, DistroAdmin)
admin.site.register(Patch, PatchAdmin)
User = get_user_model()
admin.site.register(User)