from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(is_active=True)
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
        # create listing
        listing = Listing(
            seller = User.objects.get(pk=request.user.id),
            starting_bid = request.POST['starting_bid'],
            category = request.POST['category'],
            title = request.POST['title'],
            description = request.POST['description'],
            image_url = request.POST['image_url']
        )
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))
    else:
        return render(request, 'auctions/create_listing.html')

def listing_view(request, listing_id, message=''):
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    current_bid = listing.bids.last()

    return render(request, 'auctions/listing.html', {
        'listing' : listing,
        'bids' : bids,
        'current_bid' : current_bid,
        'message' : message
    })

def bid_on_listing(request, listing_id):
    # get listing
    listing = Listing.objects.get(pk=listing_id)
    # get largest bid
    try:
        # the largest bid must always be last
        current_bid_amount = listing.bids.last().amount
    except AttributeError:
        # if bids is empty, current_bid = starting_bid
        current_bid_amount = listing.starting_bid
    # if posted bid > current bid
    bid_amount = int(request.POST['bid_amount'])
    if bid_amount > current_bid_amount:
        # create new bid and save it
        new_bid = Bid(
            listing = listing,
            bidder = User.objects.get(pk=request.user.id),
            amount = bid_amount
        )
        new_bid.save()
        # successfully redirect back to the listing's page
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))
    else:
        # reload page with an error
        messages.info(request, 'Your bid has to be higher than current bid!')
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))