from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    CATEGORY_CHOICES = [
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Books", "Books"),
        ("Sports", "Sports"),
        ("Jewelry", "Jewelry"),
        ("Art", "Art"),
        ("Collectibles", "Collectibles"),
        ("Automotive", "Automotive"),
        ("Garden", "Garden"),
        ("Music", "Music"),
        ("Movies", "Movies"),
        ("Gaming", "Gaming"),
        ("Health", "Health"),
        ("Beauty", "Beauty"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=64, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="listings", null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="won_listings", null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.seller.username}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bidder.username} bid {self.amount} on {self.listing.title}"


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.commenter.username} commented on {self.listing.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchers")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"

