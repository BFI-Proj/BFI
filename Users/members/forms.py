from django import forms
from .models import FoodItem, Review
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'ingredients', 'category', 'image', 'description']  # Include the 'image' field

class FoodItemSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search for Food')
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']