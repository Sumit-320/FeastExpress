from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import message,EmailMessage
from django.conf import settings

# utility functions to use accross app
def detect(user):
    if user.type==1:  # for seller (type=1 in models.py)
        redirect_url='vendorDashboard'
        return redirect_url
    elif user.type==2: # for customer (type=2 in models.py)
        redirect_url='customerDashboard'
        return redirect_url
    elif user.type==None and user.is_superadmin:
        redirect_url='/admin'
        return redirect_url
    
def send_email(request,user,mail_subject,mail_template):
    email_sender= settings.DEFAULT_FROM_EMAIL
    curr_site= get_current_site(request) #to fetch the current site based on the incoming request
    # render_to_string: utility fun to render HTML email template to string
    message = render_to_string(mail_template,{ 
        'user':user,
        'domain':curr_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),# (encoded) string representing the user's primary key
        'token': default_token_generator.make_token(user), # otp type
    })
    to_email= user.email
    mail = EmailMessage(mail_subject,message,email_sender,to=[to_email]) #creates an instance of Django's EmailMessage class
    mail.send()

def reset_link(request,user,mail_subject,mail_template):
    email_sender= settings.DEFAULT_FROM_EMAIL
    curr_site= get_current_site(request) #to fetch the current site based on the incoming request
    # render_to_string: utility fun to render HTML email template to string
    message = render_to_string(mail_template,{ 
        'user':user,
        'domain':curr_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),# (encoded) string representing the user's primary key
        'token': default_token_generator.make_token(user), # otp type
    })
    to_email= user.email
    mail = EmailMessage(mail_subject,message,email_sender,to=[to_email]) #creates an instance of Django's EmailMessage class
    mail.send()

def send_notification(mail_subject,mail_template,context):  # this util func is used at many places-- application approval/rejection etc.
    email_sender = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email = context['user'].email  # accessing dict keys (context)
    mail = EmailMessage(mail_subject,message,email_sender,to=[to_email])
    mail.send()