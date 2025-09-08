from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment,  WatchList
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    active_listings = Listing.objects.filter(status="Active")
    return render(request, "auctions/index.html", {
        "listings" : active_listings,
        "page_title": "Active Listings"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            lsiting_new_obj = form.save(commit=False)
            lsiting_new_obj.owner = request.user
            lsiting_new_obj.highest_bid = lsiting_new_obj.starting_bid
            lsiting_new_obj.save()
            return HttpResponseRedirect(reverse("listing", kwargs=({"id" : form.instance.id})))
        else:
            print(form.errors)
    else:
        new_listing_form = ListingForm()
        return render(request, "auctions/create.html", {
            "listing_form" : new_listing_form
        })
    
def view_listing(request, id):
    listing = Listing.objects.get(pk=id)
    user_watchlist = WatchList.objects.filter(watcher=request.user).values_list('watched_listing__id' ,flat=True)
    comments = Comment.objects.filter(on=listing)
    
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "categories" : listing.category,
        "bid_form" : BidForm(),
        "watched_listing_ids" : user_watchlist,
        "comment_form" : CommentForm(),
        "comments": comments
    })
    
@login_required
def place_bid_view(request, id):
    listing_obj = Listing.objects.get(pk=id)
    
    if request.method=="POST":
        bid_form = BidForm(request.POST)
        
        if bid_form.is_valid():
            # validate bid amount
            bid_instance = bid_form.save(commit=False)
            bid_instance.bidder = request.user
            bid_instance.listing = listing_obj
            
            if bid_instance.amount_validator() and bid_instance.is_highest():
                listing_obj.highest_bid = bid_instance.amount
                print(listing_obj.highest_bid)
                print(bid_instance.amount)
                listing_obj.save()
                messages.success(request, "Your bid was successfuly placed!")
                bid_form.save()
                return HttpResponseRedirect(reverse("listing", kwargs={"id":id}))
            
            else:
                messages.warning(request, f"Your bid ${bid_instance.amount} must be more than starting bid ${bid_instance.listing.starting_bid}  and highest bid ${bid_instance.listing.highest_bid}")
                return render(request, "auctions/listing.html", {
                    "listing" : listing_obj,
                    "categories" : listing_obj.category.all(),
                    "bid_form" : bid_form,
                })
        

@login_required        
def close_listing_view(request, id):
    listing_obj = Listing.objects.get(pk=id)
    
    if request.user == listing_obj.owner:
        listing_obj.status = "Closed"
        winner_bid = Bid.objects.get(amount = listing_obj.highest_bid, listing = id)
        listing_obj.winner = winner_bid.bidder
        listing_obj.save()
        messages.success(request, "Your Listing was successfully closed!")
    
    else:
        messages.warning(request, "Only the Owner of this Listing can close it.")
        
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


@login_required
def modify_watchlist_view(request, id):
    if request.method == "POST":
        
        listing_obj = Listing.objects.get(pk=id)
        if request.POST["action"] == "add":
            new_watchlist_obj = WatchList.objects.create(
                watcher = request.user,
                watched_listing = listing_obj
                )
            new_watchlist_obj.save()
        
            messages.info(request, "The Listing was successfully added to your watchlist.")
        elif request.POST["action"] == "remove":
            watch_list_obj = WatchList.objects.get(
                watcher = request.user,
                watched_listing = listing_obj
            )
            watch_list_obj.delete()
            messages.info(request, "The Listing was successfully removed from your watchlist.")
        
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))

@login_required
def add_comment_view(request, id):
    if request.method == "POST":
        listing_obj = Listing.objects.get(pk=id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.on = listing_obj
            comment.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))
        
@login_required        
def watchlist_view(request):
    user_watchlists = WatchList.objects.filter(watcher=request.user)
    listings_on_user_watchlist = [watchlist.watched_listing for watchlist in user_watchlists]
    
    return render(request, "auctions/index.html", {
        "listings" : listings_on_user_watchlist,
        "page_title": "Watchlist"
    })
    
def categories_view(request):
    categories = Listing.objects.values_list("category", flat=True).distinct().exclude(category__isnull=True)
    
    categories_empty = True  if all(category == "" for category in categories) else False
    
    return render(request, "auctions/categories.html", {
        "categories" : categories,
        "empty" : categories_empty
    })
    
def category_view(request, category_name):
    
    listings_in_category = Listing.objects.filter(category=category_name)
    return render(request, "auctions/index.html", {
        "listings" : listings_in_category,
        "page_title": category_name
    })