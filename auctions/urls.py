from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listings/<listing_id>', views.listing_view, name='listing'),
    path('bid_on_listing/<listing_id>',
         views.bid_on_listing, name='bid_on_listing'),
    path("comment_on_listing/<listing_id>",
         views.comment_on_listing, name="comment_on_listing"),
    path('close_listing/<listing_id>', views.close_listing, name="close_listing"),
    path('categories', views.categories, name="categories"),
    path('category/<category>', views.category_listings, name="category_listings"),
    path('watch/<listing_id>', views.toggle_watchlist, name="toggle_watchlist"),
    path('watchlist', views.watchlist_view, name="watchlist")
]
