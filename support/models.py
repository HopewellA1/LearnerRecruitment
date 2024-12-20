from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class query(models.Model):
    queryId = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="support_messages",null=True, blank=True )
    name = models.CharField(max_length=60, default='default_name')
    surname = models.CharField(max_length=60, default='default_name')
    email = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
        