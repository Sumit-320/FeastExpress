from django.contrib import admin
from .models import User,Profile2
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomAdmin(UserAdmin):
      # list_display includes the fields that are present in the User model
    list_display = ('username', 'email', 'f_name', 'l_name', 'type','is_admin')
    ordering = ('-date_of_register',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,CustomAdmin)
admin.site.register(Profile2)