from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.redirectAccount), 
    path('signup/',views.registerUser,name='signup'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/',views.login,name='login'),
    #path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
    path('customerDashboard/',views.customerDashboard,name='customerDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    path('redirectAccount/',views.redirectAccount,name='redirectAccount'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('resetAccountPassword/',views.resetAccountPassword,name='resetAccountPassword'),
    path('resetValidate/<uidb64>/<token>/',views.resetValidate,name='resetValidate'),
    path('vendor/',include('vendor.urls')),
    #path('customer/',include('customer.urls')),
]
