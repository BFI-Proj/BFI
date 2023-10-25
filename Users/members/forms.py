from django import forms
from .models import FoodItem
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'ingredients', 'category', 'image']  # Include the 'image' field

class FoodItemSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search for Food')
    
