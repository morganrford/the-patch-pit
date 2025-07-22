from django.contrib import admin
from .models import Distro, Patch

class DistroAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Distro, DistroAdmin)
admin.site.register(Patch, PatchAdmin)

