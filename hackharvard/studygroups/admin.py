from django.contrib import admin

from . import models

admin.site.register(models.Course)
admin.site.register(models.Profile)
admin.site.register(models.DateDuration)
admin.site.register(models.Group)
# Register your models here.
