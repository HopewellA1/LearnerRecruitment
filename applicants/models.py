from django.db import models
from django.contrib.auth.models import User





class Company(models.Model):
    
    CompanyId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=20)
    Email = models.CharField(max_length=60)
  
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

      
    
class Depertment(models.Model):
    DepertmentId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Company = models.ForeignKey(Company,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Exac = models.ForeignKey(Exac,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Name = models.CharField(max_length=60)
    

class category(models.Model):
    categoryId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    categoryName = models.TextField()
    

class Learner(models.Model):
    ApplicantId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#added by who
    Depertment = models.ForeignKey(Depertment,blank=True,null=True,on_delete=models.CASCADE)#added by who
    category = models.ForeignKey(category,blank=True,null=True,on_delete=models.CASCADE)#added 
    LearnerIDNumber = models.CharField(max_length=13)
    DOB = models.DateField(blank=False, null=False)
    Gender = models.CharField(max_length=6, blank=False, null=False)
    EquityCode = models.CharField(max_length=12, blank=False, null=False)
    NationalityCode= models.CharField(max_length=60, default='South Africa', blank=False, null=False)
    HomeLanguage = models.CharField(max_length=15, blank=False, null=False)
    LearnerSurname = models.CharField(max_length=60, blank=False, null=False)
    LearnerFirstName = models.CharField(max_length=60, blank=False, null=False)
    LearnerMiddleName = models.CharField(max_length=60,blank=True, null=True)
    LearnerHomeAddress1 = models.CharField(max_length=100, blank=False, null=False)
    LearnerHomeAddress2 = models.CharField(max_length=100, blank=True, null=True)
    #LearnerHomeAddress3 = models.CharField(max_length=100, blank=True, null=True)
    Municipality = models.CharField(max_length=50, blank=False, null=False)
    LearnerHomePostalCode =  models.CharField(max_length=6, blank=False, null=False)
    STATSSAArea =  models.CharField(max_length=30, blank=True, null=True)
    LearnerCellPhoneNumber =  models.CharField(max_length=30, blank=False, null=False)
    LearnerFaxNumber = models.CharField(max_length=30, blank=True, null=True)
    LearnerEmailAddress = models.CharField(max_length=10, blank=True, null=True)
    Province = models.CharField(max_length=50, blank=False, null=False)
    Disability = models.CharField(max_length=10,default='no')
    LastSchoolEMISNo = models.CharField(max_length=30, blank=False, null=False)
    LastSchoolName = models.CharField(max_length=100)
    LastSchoolYear = models.IntegerField()
    DegreeTitle = models.CharField(max_length=50, null=True)
    FieldOfStudy = models.CharField(max_length=60)
    NQFLevel = models.IntegerField()
    RACE = models.CharField(max_length=40)
    Institution = models.CharField(max_length=60)
    MajorSubjects = models.TextField(default="None")
    Experience = models.TextField(default= "None")
    isSigned = models.BooleanField(default=False)
    
    Status = models.CharField(max_length=60, default="Available")
    
