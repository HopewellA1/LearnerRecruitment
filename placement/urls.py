from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    #path('contact/', views.contact, name="contact")
    path('report', views.report, name="report"),
    path('download_category_report/<int:categoryId>', views.download_category_report, name="download_category_report")
]