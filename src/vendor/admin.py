from django.contrib import admin
from .models import Vendor, OpeningHour
# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','name','is_approved','created_at')
    list_display_links= ('user','name')
    list_editable = ('is_approved',) # in case to terminate a license!
class OpeningHourAdmin(admin.ModelAdmin):
    list_display=('vendor','day','from_hour','to_hour')
admin.site.register(Vendor,VendorAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)

