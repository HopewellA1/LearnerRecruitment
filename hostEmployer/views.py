from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from applicants.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site


@login_required
def companyDashboard(request):
    
    user = request.user
    try:
        exac = get_object_or_404(Exac, user = user)
    except:
        messages.error(request, "You have not joined any company you can add your company or select below")
        return redirect("SelectCompany")
    
    company = exac.Company
    return redirect("departments", CompanyId= company.CompanyId )
        
    
    
@login_required
def SelectCompany(request):
    user = request.user
    
    
    companies = Company.objects.all()
    if request.method == 'GET':
        
        payload = {
            "companies":companies
        }
        return render(request, 'hostEmployer/SelectCompany.html', payload)
    
    
    if request.method == 'POST':
        
        company = Company.objects.create(
            user  = user,
            Name = request.POST["Name"],
            Phone = request.POST["Phone"],
            Email = request.POST["Email"]
        )
        
        messages.success(request, 'The company details have been added successfully. Add your management details.')
        return redirect('addManagement',CompanyId =company.CompanyId )
    
@login_required  
def addManagement(request,CompanyId):
    company = get_object_or_404(Company, pk = CompanyId)
    user = request.user
    
    if request.method =='GET':
        
        payload = {
           "company": company, 
        }
        
        return render(request, 'hostEmployer/addManagement.html', payload)
    
    if request.method == 'POST':
        
        exac = Exac.objects.create(
            user = user,
            Company = company,
            FirstName = request.POST["FirstName"],
            LastName = request.POST["LastName"],
            Gender = request.POST["Gender"],
            Position = request.POST["Position"],
            EmailAddress = request.POST["EmailAddress"],
            PhoneNumber = request.POST["PhoneNumber"],
            Address = request.POST["Address"],   
        )
        
        messages.success(request, 'Manager details added successfully, please add or select your department to add learners.')
        return redirect('departments', CompanyId = CompanyId)
    
    
@login_required   
def departments(request, CompanyId):
    
    company = get_object_or_404(Company, pk = CompanyId)
    Departments = Department.objects.filter(Company = company)
    departments = []
    try:
        exac = get_object_or_404(Exac, user = request.user)
    except:
        exac = None        
    for department in Departments:
        departments.append(
            {
               "department":  department,
               "numLearners": calcList(Learner.objects.filter(Department=department)),
               
            }
        )
        

    
    if request.method == 'GET':
        
        payload = {
            "company": company,
            "departments":departments,
            "exac": exac
            
        }
        
        return render(request, 'hostEmployer/departments.html', payload)
    
    if request.method == 'POST':
        
        department = Department.objects.create(
            Company = company,
            Exac= exac,
            Name = request.POST["Name"],
            Description = request.POST["Description"]   
        )
        messages.success(request, "Department added, you may add learners to department")
        return redirect("departments",CompanyId = company.CompanyId )
@login_required   
def DepartmentLearners(request,departmentId):
    try:
        department = get_object_or_404(Department, pk = departmentId)
    except:
        messages.error(request, "The department you are trying to access was not found.")
        return redirect("companyDashboard")
    company = department.Company
    try:
        exac = get_object_or_404(Exac, user = request.user)
    except:
        exac = None
    learners = Learner.objects.filter(Department = department, Status="Recruited") 
    if request.method == 'GET':
        
        payload = {
           "learners": learners,
            "department": department,
            "company":company,
            "exac": exac
        }
        
        return render(request, 'applicants/learners.html', payload)
    
    
@login_required
def selectCategory(request, departmentId):
    
    user = request.user
    
    try:
        department = get_object_or_404(Department, pk = departmentId)  
    except:
        messages.error(request, 'The department you tried to access was not found')
        return redirect('companyDashboard')  
    Categories = category.objects.all()
    print("Categories: ", Categories)
    payload = {
        "department": department,
        "categories": Categories
    }
    return render(request, 'hostEmployer/selectCategory.html', payload)


def selectLearner(request, departmentId, categoryId):
    try:
        department = get_object_or_404(Department, pk = departmentId)  
    except:
        messages.error(request, 'The department you tried to access was not found')
        return redirect('companyDashboard') 
    Category = get_object_or_404(category, pk= categoryId)
    learners = Learner.objects.filter(category = Category)
    if request.method == 'GET':
        
        payload = {
           "learners": learners,
            "Category": Category,
            "department": department,
            "selectState":True
        }

        return render(request, 'applicants/learners.html', payload)

def ConfirmLearner(request, learnerId, departmentId):
    try:
        department = get_object_or_404(Department, pk = departmentId)  
    except:
        messages.error(request, 'The department you tried to access was not found')
        return redirect('companyDashboard')
    
    try:
        learner = get_object_or_404(Learner, pk=learnerId)
    except:
        messages.error(request, 'The learner you tried to access was not found')
        return redirect('companyDashboard')
    Category = learner.category
    try:
        exac = get_object_or_404(Exac, user = request.user)
    except:
        messages.error(request, "You must be a manager to take this action.")
        return redirect("home")

    if request.method == 'GET':
        
        payload = {
            "learner": learner,
            "Category":Category,
            "department":department,
            "selectState":True
        }
        messages.warning(request, f"Are you sure you want to add this learner to you department({department.Name})?")
        return render(request, 'applicants/learnerDetails.html',payload )
    
    if request.method == 'POST':
        
        learner.Status = "Recruited"
        learner.Exac = exac
        learner.Department = department
        learner.save()
        
        messages.success(request, "The Learner has been added to the department")
        return redirect("selectLearner", departmentId = department.DepartmentId , categoryId =learner.category.categoryId )
@login_required      
def confirmRemoval(request, learnerId):
    
    try: 
        learner =get_object_or_404(Learner, pk =learnerId )
    except:
        messages.error(request, "The learner you tried to access was not found")
        return redirect("companyDashboard")
    
    department = learner.Department
    Category = learner.category
    
    if request.method == 'GET':
        payload = {
            "learner": learner,
            "Category":Category,
            "department":department,
            "is_remove":True
        }
        
        messages.warning(request, f"Are you sure you want to remove this learner from the department of {department.Name} at {department.Company.Name}")
        return render(request, 'applicants/learnerDetails.html',payload)

    
    if request.method == 'POST':
    #removing learner
        learner.Department = None
        learner.Exac = None
        learner.Status = "Available"
        learner.save()
        messages.success(request, "The learner has been removed from the department")
        return redirect("DepartmentLearners", departmentId = department.DepartmentId )
    
def calcList(list):
    numObj = 0
    for obj in list:
        numObj +=1
    return numObj



#compnay CRUD

def companyDetails(request, companyId):
    
    try:
        company = get_object_or_404(Company, pk = companyId)
    except:
        messages.error(request, "The record you tried to access was not found")
        return redirect("home")
    
    try:
        exac = get_object_or_404(Exac, user = request.user,Company=company)
    except:
        exac = None    

    All_Exacs = Exac.objects.filter(Company = company)
    
    
    if request.method == 'GET':
        
        payload = {
            "company":company,
            "exac":exac  ,
            "All_Exacs":All_Exacs,
            "numManagers":calcList(All_Exacs) ,
            "numLearners":  calcCompanyLeanrners(company.CompanyId)
        }
        return render(request, 'hostEmployer/companyDetails.html', payload)
        

def calcCompanyLeanrners(companyId):
    nunLearners = 0
    for dep in Department.objects.filter(Company = get_object_or_404(Company, pk = companyId)):
        nunLearners += calcList(Learner.objects.filter(Department=dep))  
    return nunLearners
    
    
         
def EditCompany(request, companyId):
    try:
        company = get_object_or_404(Company, pk = companyId)
    except:
        messages.error(request, "The record you tried to access was not found")
        return redirect("home")
    
    try:
        exac = get_object_or_404(Exac, user = request.user,Company=company)
    except:
        exac = None    

    
    
    if request.method == 'GET':
        
        payload = {
            "company":company,
            "exac":exac   
        }
        return render(request, 'hostEmployer/EditCompany.html', payload)
    
    
    if request.method == 'POST':
        
        company.Name = request.POST["Name"]
        company.Phone = request.POST["Phone"]
        company.Email = request.POST["Email"]
        company.Address = request.POST["Address"]
        
        company.save()
        messages.success(request, "Changes saved successfully.")
        return redirect("companyDetails", companyId=company.CompanyId)
         
    
    
def departmentDetails(request, departmentId):
    
    try:
        department = get_object_or_404(Department, pk = departmentId)
    except:
        messages.error(request, "The department you tried to access was not found.")
        return redirect("home")
   
    try:
        exac = get_object_or_404(Exac, user = request.user,Company=company)
    except:
        exac = None
    
    company = department.Company
    otherDepartments =[]
    Departments = Department.objects.filter(Company = company)
    for department in Departments:
        otherDepartments.append(
            {
               "department":  department,
               "numLearners": calcList(Learner.objects.filter(Department=department)),
               
            }
        )
    if request.method == 'GET':
        
        payload = {
            "department": department,
            "company": company,
            "exac":exac,
            "otherDepartments":otherDepartments
            
        }
        return render(request, 'hostEmployer/departmentDetails.html', payload)
    
    if request.method == 'POST':
        
        department.Name = request.POST["Name"]
        department.Description = request.POST["Description"]
        department.save()
        messages.success(request, "Changes have been saved.")
        return redirect("departmentDetails", departmentId=department.DepartmentId)
         
def CompanyLearners(request, CompanyId):
    
    try:
        company = get_object_or_404(Company, pk = CompanyId)
    except:
        messages.error(request, "The records you tried to access were not found.") 
        return redirect("home")
    payload = {
        "learners": getCompanyLearners(company.CompanyId),
        "company":company
    }
    return render(request, 'hostEmployer/CompanyLearners.html', payload)
    
       
def getCompanyLearners(CompanyId):
    company = get_object_or_404(Company, pk = CompanyId) 
    learners = []
    deps = Department.objects.filter(Company= company)
    for dep in deps:
        for learner in Learner.objects.filter(Department = dep):
            learners.append(learner)
    return learners

@login_required 
def Searchbar(request, **kwargs):
    if request.method == "POST":
        Learners = []
        companyId = request.POST.get('companyId')
        
        if companyId:
            company = get_object_or_404(Company, pk = companyId)
            Searched = request.POST['Searched'].strip()
            print("Searched: ", Searched)
            firstNameSearch = Learner.objects.filter(
                Company = company,
                LearnerFirstName__contains=Searched,
                LearnerSurname__contains=Searched,
                NQFLevel__contains=Searched,
                                                    )
       
        
        for learner in firstNameSearch:
            Learners.append(learner)
        
            
        print("Learners: ", Learners)
        return render(request, 'hostEmployer/Searchbar.html', {'searched': Searched, 'Learners': Learners})
    else:
        return render(request, 'hostEmployer/Searchbar.html', {'searched': '', 'Learners': []})


    
    
    
        
        
        
