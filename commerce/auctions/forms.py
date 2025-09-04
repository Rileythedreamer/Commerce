from django.forms import ModelForm
from .models import Listing
from django import forms


class Listing_Form(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'image_url',
            "category",
            'highest_bid',
        ]
        labels = {
            'title' : 'Title',
            'description' : 'Description',
            'image_url' : 'Image',
            'highest_bid' : 'Starting Bid',
            'category' : 'Category'
        }
        widgets = {
            'title': forms.TextInput(attrs=({'class':'form-control w-75', })),
            'description': forms.Textarea(attrs=({'class': 'form-control w-75', 'rows': '6',})),
            'image_url': forms.URLInput(attrs=({'class':'form-control w-75', 'required':False})),
            'highest_bid': forms.NumberInput(attrs=({'class': 'form-control w-75'})),
            'category' : forms.TextInput(attrs=({'class':'form-control w-75', }))
        }

