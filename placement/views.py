from django.shortcuts import render, redirect, get_object_or_404
from applicants.models import *


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
        company = get_object_or_404(Company, pk =companyId )
        print(company.Name, " :: company")
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
            "Category":Category,
            "Comapnies": findComps(Category),
            "Analytics": getCategoryAnalytics(Category.categoryId), 
        }
        return CategoryCompanies
    except:
        return None

def findComps(categ):
   
    companies = []
    comps = Company.objects.all()
    
    for comp in comps:
        print("comps:::::: ",comp)
        compAnalytic = getCompanyAnalytics(comp.CompanyId)
        deps = compAnalytic.departments
        #deps = Department.objects.filter(Company = comp)
        print("CategorycategId, categ: ", categ) 
        departments = []
        for dep in deps:
            learners = Learner.objects.filter(Department = dep.department, category = categ)
            if countObj(learners) > 0:
                departments.append({
                    "department": dep,
                    "learners":learners
                })
            
        if countObj(departments) > 0:
            companies.append({
                "Company":comp,
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
    