from django.db import models
from register.models import User,Profile2
from register.utils import send_notification
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
    
    def save(self,*args,**kwargs):  # when we dont know no. of arguments initially
        if self.pk is not None:
            original = Vendor.objects.get(pk=self.pk)  # initial state of user's class 
            if original.is_approved!=self.is_approved: # means there is a change
                mail_template= 'email/vendorApproval.html'
                context = {    # data to provide to the html file
                    'user':self.user,
                    'is_approved':self.is_approved,
                }
                if self.is_approved==True: # means vendor approved
                    mail_subject = 'Congrats, your restaurant is approved!'
                    
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject = 'Sorry, your vendor application was rejected!'
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs) # detects a change in class


