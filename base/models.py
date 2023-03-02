from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']

class Location(models.Model):
    # ID, Name, Image, Description, Ages, Category, SubCategories, Opening Hours, Address, Other Info
    #locid = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    # name, description, price if available, category, open hours, address
    name = models.CharField(max_length=200, primary_key=True)
    image = models.CharField(max_length=250)
    description = models.TextField()
    ages = models.CharField(max_length=100)
    price = models.CharField(max_length=200)
    category = models.CharField(max_length=150)
    subCategories = models.TextField()
    openhours = models.TextField()
    address = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=100, decimal_places=6,default=25.750156)
    lon = models.DecimalField(max_digits=100, decimal_places=6,default=-80.27964)
    #lat = models.CharField(max_length=40,default="2")
    #lon = models.CharField(max_length=40,default="3")
    other_info = models.TextField()

    