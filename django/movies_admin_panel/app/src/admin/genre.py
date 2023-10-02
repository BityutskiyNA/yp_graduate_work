from django.contrib import admin
from src.models.genre import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "updated_at")
