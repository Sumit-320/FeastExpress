from django.urls import path,include
from . import views
from register import views as registerViews
urlpatterns = [
    path('', registerViews.vendorDashboard,name='vendor'),
    path('profile/',views.vProfile,name='vProfile'),
]