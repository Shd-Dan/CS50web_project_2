from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Category, Listing


def index(request):
    # Query data from database
    all_listings = Listing.objects.all().values()
    # Pass the listings to a template for display
    # Return the rendered template with the listings
    return render(request, "auctions/index.html", {"all_listings":all_listings})


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
    
