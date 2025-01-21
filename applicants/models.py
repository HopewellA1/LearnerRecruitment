from django.db import models
from django.contrib.auth.models import User





class Company(models.Model):
    
    CompanyId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=20)
    Email = models.CharField(max_length=60)
    Address = models.CharField(max_length=100, default='None')
    
class Exac(models.Model):
    Management = models.AutoField(primary_key=True,blank=False, null=False, auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Position = models.CharField(max_length=50)
    Company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE)#added by who
    FirstName = models.CharField(max_length=60)
    LastName = models.CharField(max_length=60)
    Gender = models.CharField(max_length=10, null=False)
    EmailAddress = models.CharField(max_length=60)
    PhoneNumber= models.CharField(max_length=20)
    Address = models.CharField(max_length=100)

      
    
class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Exac = models.ForeignKey(Exac,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=300, default='None')
    is_Recruited = models.BooleanField(default=True)
    

class category(models.Model):
    categoryId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    categoryName = models.CharField(max_length=100 )
    description = models.CharField(max_length=500, default="N/A")
    code = models.CharField(max_length=15, default='None')
    

class Learner(models.Model):
    ApplicantId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Department = models.ForeignKey(Department,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Exac = models.ForeignKey(Exac,blank=True,null=True,on_delete=models.CASCADE)#added by who
    category = models.ForeignKey(category,blank=True,null=True,on_delete=models.CASCADE)#added 
    LearnerIDNumber = models.CharField(max_length=13)
    DOB = models.DateField(blank=True, null=True)
    Gender = models.CharField(max_length=6, blank=False, null=False)
    EquityCode = models.CharField(max_length=12, blank=True, null=True, default="N/A")
    NationalityCode= models.CharField(max_length=60, default='South Africa', blank=False, null=False)
    HomeLanguage = models.CharField(max_length=15, blank=False, null=False)
    LearnerSurname = models.CharField(max_length=60, blank=False, null=False)
    LearnerFirstName = models.CharField(max_length=60, blank=False, null=False)
    LearnerMiddleName = models.CharField(max_length=60,blank=True, null=True)
    LearnerHomeAddress1 = models.CharField(max_length=100, blank=False, null=False)
    LearnerHomeAddress2 = models.CharField(max_length=100, blank=True, null=True, default="N/A")
    #LearnerHomeAddress3 = models.CharField(max_length=100, blank=True, null=True)
    Municipality = models.CharField(max_length=50, blank=False, null=False)
    LearnerHomePostalCode =  models.CharField(max_length=6, blank=False, null=False)
    STATSSAArea =  models.CharField(max_length=30, blank=True, null=True)
    LearnerCellPhoneNumber =  models.CharField(max_length=50, blank=False, null=False)
    LearnerFaxNumber = models.CharField(max_length=30, blank=True, null=True)
    LearnerEmailAddress = models.CharField(max_length=100, blank=True, null=True)
    Province = models.CharField(max_length=50, blank=False, null=False)
    Disability = models.CharField(max_length=10,default='no')
    LastSchoolEMISNo = models.CharField(max_length=30, blank=False, null=False)
    LastSchoolName = models.CharField(max_length=100)
    LastSchoolYear = models.IntegerField(blank=True, null=True)
    DegreeTitle = models.CharField(max_length=200, null=True)
    FieldOfStudy = models.CharField(max_length=60)
    NQFLevel = models.CharField(max_length=5)
    RACE = models.CharField(max_length=40)
    Institution = models.CharField(max_length=60)
    MajorSubjects = models.TextField(default="None")
    Experience = models.TextField(default= "None")
    isSigned = models.BooleanField(default=False)
    
    Status = models.CharField(max_length=60, default="Available")
    
