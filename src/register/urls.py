from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.registerUser,name='signup'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/',views.login,name='login'),
    path('dashboard/',views.login,name='dashboard'),
]
