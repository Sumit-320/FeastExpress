from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ['username','f_name','l_name','contact','email','password','confirm_password']

    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password= cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError("Your passwords do not match!")
            