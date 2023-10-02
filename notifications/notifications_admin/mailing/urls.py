from django.urls import path
from . import views

urlpatterns = [
    path('process_mailing/<int:pk>/', views.process_mailing, name='process_mailing'),
    path('system_events/<str:name>/', views.SystemEventsView.as_view(), name='system_events'),
    path('mailing_type/<int:pk>/', views.MailingTypeView.as_view(), name='mailing_type'),
    path('planet_mailing/', views.PlannedMailingView.as_view(), name='planet_mailing'),
]
