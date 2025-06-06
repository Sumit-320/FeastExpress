from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Profile2
# this is triggered on signal (when user is created) in order to automatically create user profile    
# @receiver(post_save, sender=User)
# def create_profile_rx(sender,instance,created,**kwargs):
#     if created:
#         Profile2.objects.create(user=instance)
#         print("Profile created successfully") 
#     else: 
#         try:
#             profile = Profile2.objects.get(user=instance)
#             profile.save()
#             print("User profile updated successfully")
#         except:
#              Profile2.objects.create(user=instance)
#              print("Profile updated successfully after creating!!") 