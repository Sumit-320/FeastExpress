from django import forms

from .models import Category
#vendor of model category is the request.user
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description'] # attributes from model 'Category' that u want in your form