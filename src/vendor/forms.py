from django import forms
from .models import Vendor, OpeningHour
from register.validators import allow_only_images_validator
class VendorForm(forms.ModelForm):
    license = forms.FileField(widget=forms.FileInput(attrs={'class':'btnx-info'}),validators=[allow_only_images_validator]) # to allow only jpg/png/webp etc
    class Meta:
        model=Vendor
        fields = ['name', 'license']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model= OpeningHour
        fields = ['day','from_hour','to_hour','is_closed']
