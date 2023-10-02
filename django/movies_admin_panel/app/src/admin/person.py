from django.contrib import admin
from src.models.person import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "updated_at")
