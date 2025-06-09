from django import forms
from .models import Category


class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title',
            'id': 'listing_title'
        })
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your item...',
            'rows': 4,
            'id': 'listing_description'
        })
    )

    starting_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0',
            'id': 'listing_starting_price'
        })
    )

    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg',
            'id': 'listing_image_url'
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="-- Select Category --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'listing_category'
        })
    )