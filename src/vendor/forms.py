from django import forms
from .models import Vendor
from register.validators import allow_only_images_validator
class VendorForm(forms.ModelForm):
    license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator]) # to allow only jpg/png/webp etc
    class Meta:
        model=Vendor
        fields = ['name', 'license']
