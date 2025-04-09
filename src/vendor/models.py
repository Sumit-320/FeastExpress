from django.db import models
from register.models import User,Profile2
from register.utils import send_notification
from datetime import time
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE) #one to one field
    profile= models.OneToOneField(Profile2,related_name='userprofile',on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    vendor_slug = models.SlugField(max_length=100,unique=True)
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
DAYS = [
    (1,("Monday")),
    (2,("Tuesday")),
    (3,("Wednesday")),
    (4,("Thursday")),
    (5,("Friday")),
    (6,("Saturday")),
    (7,("Sunday")),
]
HOURS = [(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day = models.IntegerField(choices = DAYS)
    from_hour = models.CharField(choices=HOURS,max_length=10,blank=True)
    to_hour = models.CharField(choices=HOURS,max_length=10,blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day','-from_hour')
        unique_together = ('vendor','day','from_hour','to_hour')  # to check no two time slots for same day

    def __str__(self):
        return self.get_day_display()