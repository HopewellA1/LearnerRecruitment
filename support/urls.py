from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from .views import ajax_response, response_list

urlpatterns = [

    path('contact/', views.contact, name="contact"),
    path("Send_Response/<int:queryId>/", views.Send_Response, name="Send_Response"),
    path('QueryList/', views.QueryList, name="QueryList"),
    path('api/total-queries/', views.total_queries_api, name='total_queries_api'),
    path("ajax_response/", ajax_response, name="ajax_response"),
    path('response_list/', views.response_list, name="response_list"),
    path('contact/', views.contact, name="contact"),
    path('Anouncements', views.Anouncements, name="Anouncements"),
    
    #APIs
    path("searchAnouncements/<str:searched>", views.searchAnouncements, name="searchAnouncements")
]

