from django.contrib import admin

from foehn import models


@admin.register(models.Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")
    search_fields = ("name",)
