from django import forms
from .models import User
from .models import Profile2
from .validators import allow_only_images_validator # to allow only jpg/png/webp etc
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ['f_name','l_name','username','email','contact','password']

    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password= cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError("Your passwords do not match!")

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your address','required':'required'}))
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'class':'btnx-info'}),validators=[allow_only_images_validator])
    bg_pic = forms.FileField(widget=forms.FileInput(attrs={'class':'btnx-info'}),validators=[allow_only_images_validator])
    #latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=Profile2
        fields=['profile_pic','bg_pic','address','country','state','city','pin','latitude','longitude']

    def __init__(self,*args,**kwargs): 
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields: 
            if field=='latitude' or field=='longitude':
                self.fields[field].widget.attrs['readonly']='readonly'