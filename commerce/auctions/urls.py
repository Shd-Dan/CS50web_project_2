from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("add_to_watchlist", views.add_item_to_watchlist, name="add_item_to_watchlist"),
    path("delete_from_watchlist", views.delete_item_from_watchlist, name="delete_item_from_watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("close_listing/", views.close_listing_auction, name="close_listing_auction"),
    path("add_comment/", views.add_comment, name="add_comment")
]
