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
        # validate inputs ------------ TODO implement django validation
        # required - title, description, starting bid
        title = request.POST['title']
        description = request.POST['description']
        if title.strip() == "" or description.strip() == "":
            messages.error(request, "Title or description invalid.")
            return render(request, 'auctions/create_listing.html')
        # optional - category, image_url
        category = request.POST['category']
        image_url = request.POST['image_url']
        if category.strip() == "":
            category = "No Category Listed"
        if image_url.strip() == "":
            image_url = "static/auctions/no-image.png"
        # create listing
        try:
            listing = Listing(
                seller = User.objects.get(pk=request.user.id),
                starting_bid = request.POST['starting_bid'],
                category = category,
                title = title,
                description = description,
                image_url = image_url
            )
            listing.save()
        except IntegrityError:
            messages.error(request, "Invalid inputs.")
            return render(request, 'auctions/create_listing.html')
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))
    else:
        return render(request, 'auctions/create_listing.html')

def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    current_bid = listing.bids.last()
    comments = listing.comments.all()
    return render(request, 'auctions/listing.html', {
        'listing' : listing,
        'bids' : bids,
        'current_bid' : current_bid,
        'comments' : comments
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
        messages.error(request, 'Your bid has to be higher than current bid!')
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))

def comment_on_listing(request, listing_id):
    # get listing and author
    listing = Listing.objects.get(pk=listing_id)
    author = User.objects.get(pk=request.user.id)
    # validate comment
    content = request.POST["posted_comment_content"]
    if content.strip() == "":
            messages.error(request, "Cannot post empty comment.")
            return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))
    try:
        comment = Comment(
            listing = listing,
            author = author,
            content = content
        )
        comment.save()
    except IntegrityError:
        messages.error(request, "Comment invalid.")
        return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))
    
    return HttpResponseRedirect(reverse('listing', args=(listing.pk,)))

def close_listing(request, listing_id):
    # get listing
    listing = Listing.objects.get(pk=listing_id)
    try:
        listing.buyer = listing.bids.last().bidder
        messages.success(request, f"Listing sold to {listing.buyer.username} for ${listing.bids.last().amount}!")       
    except AttributeError:
        messages.warning(request, "No bids have been placed, listing closed with no buyer.")
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse('index'))