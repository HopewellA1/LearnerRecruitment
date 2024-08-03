from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from applicants.models import *




def SelectCompany(request):
    user = request.user
    if user.is_staff:
        messages.error(request, "You are not allowd to access this part.")
        return redirect("home")
    
    companies = Company.objects.all()
    if request.method == 'GET':
        
        payload = {
            "companies":companies
        }
        return render(request, 'hostEmployer/SelectCompany.html')
        
        
        
