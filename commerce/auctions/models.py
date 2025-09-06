from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model): #optional
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    owner = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, related_name="listings",on_delete=models.SET_NULL, null=True, blank=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default="Active")
    

    def __str__(self):
        return self.title


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE) # the user who is making the bid
    listing = models.ForeignKey(Listing, related_name="bid", on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

