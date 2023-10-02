from django.contrib import admin
from django.urls import path

from discount import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/<int:pk>', views.create_token_view, name='create-object'),
]
