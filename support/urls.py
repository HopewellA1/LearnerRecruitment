from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
path('contact/', views.contact, name="contact"),
path("response/<int:queryId>/", views.response, name="response"),
path('QueryList/', views.QueryList, name="QueryList"),
path('api/total-queries/', views.total_queries_api, name='total_queries_api'),
]