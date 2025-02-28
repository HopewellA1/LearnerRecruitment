"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    
    path('SelectCompany', views.SelectCompany, name="SelectCompany"),
    path('addManagement/<int:CompanyId>', views.addManagement, name="addManagement"),
    path('departments/<int:CompanyId>', views.departments, name="departments"),
    path('DepartmentLearners/<int:departmentId>', views.DepartmentLearners, name="DepartmentLearners"),
    path('companyDashboard', views.companyDashboard, name="companyDashboard" ),
    path('selectCategory/<int:departmentId>', views.selectCategory, name="selectCategory"),
    path('selectLearner/<int:departmentId>/<int:categoryId>', views.selectLearner, name="selectLearner"),
    path('ConfirmLearner/<int:learnerId>/<int:departmentId>/', views.ConfirmLearner, name="ConfirmLearner"),
    path('confirmRemoval/<int:learnerId>',  views.confirmRemoval, name="confirmRemoval"),
    path('companyDetails/<int:companyId>', views.companyDetails, name="companyDetails"),
    path('EditCompany/<int:companyId>', views.EditCompany, name="EditCompany"),
    path('departmentDetails/<int:departmentId>', views.departmentDetails, name="departmentDetails"),
    path('CompanyLearners/<int:CompanyId>', views.CompanyLearners, name="CompanyLearners"),
    
    path('download_departmentExcel/', views.download_departmentExcel, name="download_departmentExcel"),
    path('SearchLearners', views.SearchLearners, name="SearchLearners"),
    
    #internal use API
    path('takenTour/<int:tourId>', views.takenTour, name="takenTour"),
    path("searchCompany/<str:searched>", views.searchCompany, name="searchCompany")
   
]
