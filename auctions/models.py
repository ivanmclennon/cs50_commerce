from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.username}'


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_listings")
    starting_bid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=32, default="No Category Listed")
    image_url = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name='watchlist')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', null=True)

    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=128)
