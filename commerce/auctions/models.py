from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model): #optional
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, related_name="listings",on_delete=models.SET_NULL, null=True, blank=True)
    highest_bid = models.FloatField()
    status = models.CharField(max_length=10, default="Active")

    def __str__(self):
        return self.title


# TODO
"""

class bid():
    pass

class comment():
    pass


    
"""
