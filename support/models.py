from django.db import models
from django.contrib.auth.models import User
from applicants.models import *
from django.utils import timezone

# Create your models here.

class query(models.Model):
    queryId = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True )
    name = models.CharField(max_length=60, default='default_name')
    surname = models.CharField(max_length=60, default='default_name')
    email = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Anouncement(models.Model):
    AnouncementId = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False, blank=False)
    
    category = models.ForeignKey(category,on_delete=models.DO_NOTHING,null=True, blank=True)
    
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    audiance = models.CharField(max_length=50, default="Companies")
    Date = models.DateTimeField(default=timezone.now())
    
    
    
    
        