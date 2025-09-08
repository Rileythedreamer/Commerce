from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# class Category(models.Model):  # optional
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class Listing(models.Model):
    owner = models.ForeignKey(
        User, related_name="listing", on_delete=models.CASCADE, default=None
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    highest_bid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    status = models.CharField(max_length=10, default="Active")
    winner = models.ForeignKey(User, related_name="listings_won", on_delete=models.SET_NULL, null=True, default=None)
    def __str__(self):
        return self.title

    # def is_highest(self):
    #     if listing


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(
        User, related_name="bids", on_delete=models.CASCADE
    )  # the user who is making the bid
    listing = models.ForeignKey(Listing, related_name="bid", on_delete=models.CASCADE)

    def amount_validator(self):
        return self.amount >= self.listing.starting_bid

    def is_highest(self):
        return self.amount > self.listing.highest_bid


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    on = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    watcher = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    watched_listing = models.ForeignKey(Listing, related_name="watchers", on_delete=models.CASCADE)