from django.db import models
from django.contrib.auth.models import User


class Tour(models.Model):
    TourId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True )
    Step = models.CharField(max_length=30, default="Path")
    is_taken = models.BooleanField(default=False)
    
    
    


