from django.forms import ModelForm, ValidationError
from .models import Listing,  Comment, Bid
from django import forms


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "image_url",
            "starting_bid",
            "category"
        ]
        labels = {
            "title": "Title",
            "description": "Description",
            "image_url": "Image",
            "starting_bid": "Starting Bid",
            "category": "Category"
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control  w-75",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control  w-75",
                    "rows": "4",
                }
            ),
            "image_url": forms.URLInput(
                attrs={"class": "form-control  w-75"}
            ),
            "starting_bid": forms.NumberInput(
                attrs={"class": "form-control  w-75", "step": "0.01"}
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control  w-75",
                }
            )
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid

        fields = ["amount"]
        labels = {"amount": "Bid Amount "}
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment

        fields = ["content"]
        labels = {
            'content' : ''
        }
        widgets = {
            "content" : forms.Textarea(
                attrs={
                    "class": "form-control w-100 rounded-4 ",
                    "rows": "2",
                    "placeholder": "Enter your comment here...",
                }
            )
        }
        
# class CategoryForm(ModelForm):
#     class Meta:
#         model = Category
#         fields = ["name"]
#         labels = {
#             'name' : 'Category'
#         }
#         widgets = {
#             'name': forms.TextInput(
#                 attrs={
#                     "class": "form-control w-100 rounded-4 ",
#                 }
#             )
#         }
