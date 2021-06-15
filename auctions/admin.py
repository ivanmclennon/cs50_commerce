from django.contrib import admin
from .models import User, Listing, Bid, Comment
# Register your models here.

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'bidder', 'amount')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'category', 'seller','title', 'description', 'starting_bid')

    def bids_display(self, obj):
        return ", ".join([
            bid.bidder for bid in obj.bids.all()
        ])
    bids_display.short_description = "Bids"


admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
