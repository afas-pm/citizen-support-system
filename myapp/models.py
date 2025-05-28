from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    user_type = models.CharField(max_length=30)
    view_password = models.CharField(max_length=30)
    
class Citizen(models.Model):
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=True)
    email = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=30,null=True)
    district = models.CharField(max_length=30,null=True)
    image = models.FileField(upload_to='file', null=True)
    
class Authority(models.Model):
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE)
    authority = models.CharField(max_length=30,null=True)    
    email = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=30,null=True)
    district = models.CharField(max_length=30,null=True)
    image = models.FileField(upload_to='file', null=True)
    
class Complaint(models.Model):
    citizenId = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    authorityId = models.ForeignKey(Authority, on_delete=models.CASCADE)
    title = models.CharField(max_length=30,null=True)
    description = models.CharField(max_length=30,null=True)
    complaintImage = models.FileField(upload_to='file', null=True)
    solvedImage = models.FileField(upload_to='file', null=True)
    status = models.CharField(max_length=30,null=True)
    date = models.DateField(null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)