from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(max_length=50)