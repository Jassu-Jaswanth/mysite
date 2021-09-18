from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    lastUpdated = models.CharField(max_length=100,default='')

class Repositories(models.Model):
    username = models.CharField(max_length=100,default='')
    repo_name = models.CharField(max_length=200,default='')
    stars = models.IntegerField(default=0)