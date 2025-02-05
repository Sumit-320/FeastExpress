from django.db import models
from register.models import User,Profile2
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE) #one to one field
    profile= models.OneToOneField(Profile2,related_name='userprofile',on_delete=models.CASCADE)
    name= models.CharField(max_length=40)
    license = models.ImageField(upload_to='vendor/license')  # media root already configured
    is_approved = models.BooleanField(default=False)# to sell at website
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

