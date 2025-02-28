from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from applicants.models import *
import os
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib import messages
from django.http import HttpResponse




#@login_required
def report(request):
   #Staff report page for all placements 
    
    objCategories = category.objects.all()
    Categories = []
    Companies =[]
    
    for comp in Company.objects.all():
       # print("comp: ", comp.Name)
        Companies.append(getCompanyAnalytics(comp.CompanyId))
        
    for categ in objCategories:
       
        learners = Learner.objects.filter(category = categ)
        Categories.append({
            
            "category":categ,
            "analytics":getCategoryAnalytics(categ.categoryId),
            "CategoryCompanies": getComapanyCategoryAnalytics(categ.categoryId)
        })
        
    payload  =  {
        "categories": Categories,
        "Companies":Companies
    }
    
    return render(request, 'placement/report.html',payload)
    
def generate_Report_pdf(categoryId):
    
    Category = get_object_or_404(category, pk = categoryId) 
    CategoryAnalytics = getCategoryAnalytics(Category.categoryId),
    CategoryCompanies = getComapanyCategoryAnalytics(Category.categoryId)
    CategoryAnalytics = getCategoryAnalytics(Category.categoryId)
    UWS_logo = os.path.join(settings.STATIC_ROOT, 'manageProfile/images/UWS - Logo - Cyan (0011).png')

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    center_x = width / 2
    center_y = height/2

    UWS_logo_width = 200 # Adjust as necessary
    UWS_logo_height = 70
    

    c.drawImage(UWS_logo, 200, 700, UWS_logo_width, UWS_logo_height)
    hearderText = f"{Category.categoryName} Placement Report"
    hearderText_width = c.stringWidth(hearderText, "Times-Bold", 28)
    c.setFont("Times-Bold", 28); c.drawString(center_x - hearderText_width / 2, 670, hearderText)
    
    
  
  
    
    line  = "________________________________________________________________________________________"
    line_width = c.stringWidth(line, "Times-Bold", 12)
    c.setFont("Times-Bold", 12); c.drawString(center_x - line_width / 2, 660, line)
    


    totalLearners_text = f'Total Learners: {CategoryAnalytics["totalLearners"]}' 
    totalLearners_text_width = c.stringWidth(totalLearners_text, "Times-Roman", 16)
    c.setFont("Times-Roman", 16); c.drawString(center_x - totalLearners_text_width / 2, 620, totalLearners_text)
    
    
    
    RecruitedLearners_text = f'Recruited Learners: {CategoryAnalytics["numRecruited"]}' 
    RecruitedLearners_text_width = c.stringWidth(RecruitedLearners_text, "Times-Roman", 16)
    c.setFont("Times-Roman", 16); c.drawString(center_x - RecruitedLearners_text_width / 2, 600, RecruitedLearners_text)
    
    AvailableLearners_text = f'Available Learners: {CategoryAnalytics["numAvailble"]}' 
    AvailableLearners_text_width = c.stringWidth(AvailableLearners_text, "Times-Roman", 16)
    c.setFont("Times-Roman", 16); c.drawString(center_x - AvailableLearners_text_width / 2, 580, AvailableLearners_text)
    
    c.setFont("Times-Bold", 12); c.drawString(center_x - line_width / 2, 550, line)
    
    
    subHeader_text = "Companies that recruited from category"
    subHeader_text_width = c.stringWidth(subHeader_text, "Times-Bold", 20)
    c.setFont("Times-Bold", 20); c.drawString(center_x - subHeader_text_width / 2, 530, subHeader_text)
    
    
    
    #water mark
    # c.saveState()
    # c.setFillAlpha(0.3) 
    # c.restoreState()  
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
    
#@login_required  
def download_category_report(request, categoryId):
    
    try:
        Category = get_object_or_404(category, pk = categoryId)
    except:
        messages.error(request, "Category does not exist.")
        #make formal redirect
        return redirect("home")
    pdf_buffer = generate_Report_pdf(Category.categoryId)
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{Category.categoryName}_pacement_report.pdf"'
    return response  

def getCategoryAnalytics(CategoryId):

    categ = get_object_or_404(category,pk = CategoryId)
    learners = Learner.objects.filter(category = categ)
    analyticOBJ = {
        "numRecruited":countObj(learners.filter(Status = "Recruited")),
        "numAvailble": countObj(learners.filter(Status = "Available")), 
        "totalLearners":countObj(learners)
    }
    return analyticOBJ
    
def getCompanyAnalytics(companyId):
    
    try:
        company = get_object_or_404(Company, pk =companyId)
        departments = Department.objects.filter(Company = company)
        deps = []
        for dep in departments:
            deps.append(getDepLearners(dep.DepartmentId))
            
        compObj = {
            "company": company,
            "departments": deps
        }
        return compObj  
    except:
        return None
    

def getComapanyCategoryAnalytics(CategoryId):
   
    try:
        Category =  get_object_or_404(category, pk = CategoryId)
       
        CategoryCompanies = {
            
            "Comapnies": findComps(Category),
            
        }
        return CategoryCompanies
    except:
        return None

def findComps(categ):
   
    companies = []
    comps = Company.objects.all()
    
    for comp in comps:
   
        compAnalytic = getCompanyAnalytics(comp.CompanyId)
        deps = compAnalytic["departments"]
        #deps = Department.objects.filter(Company = comp)
        
        departments = []
        numLearners = 0
        for dep in deps:
            learners = Learner.objects.filter(Department = dep["department"], category = categ)
            numLearners += countObj(learners)
            if countObj(learners) > 0:
                departments.append({
                    "department": dep,
                    "learners":learners,
                    "DepnumLearners": countObj(learners)
                    
                })
            
        if countObj(departments) > 0:
            companies.append({
                "Company":comp,
                "departments": departments,
                "numLearners":numLearners
            })
    return companies
        

def getDepLearners(depId):
    try:
        department = get_object_or_404(Department,pk = depId)
    except:
        return None
    learners = Learner.objects.filter(Department = department)
    return {
        "department": department,
        "learners": learners,
        "numLearners": countObj(learners)
    }
   
def countObj(list):
    num =0
    for obj in list:
        num +=1 
    return num
    