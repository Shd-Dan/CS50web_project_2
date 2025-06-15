from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Category, Listing, Watchlist, Bid


def index(request):
    # Query data from database
    all_listings = Listing.objects.all().values()
    # Pass the listings to a template for display
    # Return the rendered template with the listings
    return render(request, "auctions/index.html", {"all_listings": all_listings})


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
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image_url = request.POST.get("image_url")
        category_id = request.POST.get("category")
        seller = request.user

        # Create listing with category if provided
        listing = Listing(
            title=title,
            description=description,
            starting_price=starting_price,
            image_url=image_url,
            seller=seller
        )

        if category_id:
            category = Category.objects.get(id=category_id)
            listing.category = category

        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        # Get categories for the form
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })


def listing_page(request, listing_id: int):
    # Query data from database
    listing = Listing.objects.get(id=listing_id)
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    # Pass the listing to a template for display
    # Return the rendered template with the listing
    return render(
        request,
        "auctions/listing_page.html",
        {"listing": listing,
         "is_in_watchlist": is_in_watchlist})


@login_required
def add_item_to_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        try:
            listing_to_add = Listing.objects.get(id=listing_id)
            user = request.user
            # Check if Watchlist exists
            if not Watchlist.objects.filter(user=user, listing=listing_to_add).exists():
                add_listing = Watchlist(
                    user=user,
                    listing=listing_to_add
                )
                add_listing.save()

        except Listing.DoesNotExist:
            pass

        return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))
    return HttpResponseRedirect(reverse("index"))


@login_required
def delete_item_from_watchlist(request):
    if request.method == "POST":
        # Get the listing_id
        listing_id = request.POST.get("listing_id")
        # Retrieve related Listing instance
        listing = get_object_or_404(Listing, id=listing_id)

        # Retrieve the watchlist item for the current user and listing
        watchlist_item_to_delete = get_object_or_404(
            Watchlist,
            user=request.user,
            listing=listing
        )
        # Delete from DB watchlist table
        watchlist_item_to_delete.delete()

        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("listing_page"))


@login_required()
def place_bid(request):
    if request.method == "POST":
        # Retrieve details from the form
        amount = request.POST["bid_amount"]
        bidder = request.user
        listing_id = request.POST.get("listing_id")

        try:
            amount = float(amount)
            listing = get_object_or_404(Listing, id=listing_id)

            print(f"Final data - Amount: {amount}, Bidder: {bidder}, Listing: {listing}")

            # Create and save bid here
            bid = Bid(
                amount=amount,
                bidder=bidder,
                listing=listing
            )
            bid.save()
            messages.success(request, "Bid placed successfully!")
            # Return appropriate response
            return redirect("listing_page", listing_id=listing_id)
        except (ValueError, TypeError):
            # Handle invalid amount
            messages.error(request, 'Please enter a valid bid amount.')
            return redirect("listing_page", listing_id=listing_id)

    return redirect("index")
