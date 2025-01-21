from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('contact/', views.contact, name="contact"),
    path('Anouncements', views.Anouncements, name="Anouncements")
]