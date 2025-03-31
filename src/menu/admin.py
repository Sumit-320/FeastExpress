from django.contrib import admin
from .models import FoodItem,Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','vendor','updated_at')
    search_fields = ('category_name','vendor__name') # foreign key to refer Vendor models' name

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title','category','vendor','price','is_available','updated_at')
    search_fields = ('food_title','category__category_name','vendor__name','price')    #  category is FK so category_name of class Category 
    list_filter = ('is_available',) # to filter out available food items 
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(Category,CategoryAdmin)
