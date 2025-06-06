from django import forms
from register.validators import allow_only_images_validator  # for png/jpg etc file formats only
from .models import Category,FoodItem
#vendor of model category is the request.user
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description'] # attributes from model 'Category' that u want in your form

# important part
class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btnx-info'}),validators=[allow_only_images_validator]) # to allow only jpg/png/webp etc

    class Meta:
        model=FoodItem
        fields=['category','food_title','description','price','image','is_available']