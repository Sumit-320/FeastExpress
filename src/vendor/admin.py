from django.contrib import admin
from .models import Vendor
# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','name','is_approved','created_at')
    list_display_links= ('user','name')
    list_editable = ('is_approved',) # in case to terminate a license!
admin.site.register(Vendor,VendorAdmin)

