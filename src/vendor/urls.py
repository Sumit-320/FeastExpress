from django.urls import path,include
from . import views
from register import views as registerViews
urlpatterns = [
    path('', registerViews.vendorDashboard,name='vendor'),
    path('profile/',views.vProfile,name='vProfile'),
    path('menu-builder/',views.menuBuilder,name='menuBuilder'),
    path('menu-builder/category/<int:pk>/',views.foodByCategories,name='foodByCategories'),
    path('menu-builder/category/add/',views.addCategory,name='addCategory'),
    path('menu-builder/category/edit/<int:pk>/',views.editCategory,name='editCategory'),
    path('menu-builder/category/delete/<int:pk>/',views.deleteCategory,name='deleteCategory'),

]
