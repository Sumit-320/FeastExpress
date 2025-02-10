from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.registerUser,name='signup'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/',views.login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
]
