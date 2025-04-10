from django.urls import path
from . import views
urlpatterns = [
    path('place-order/',views.placeOrder,name='placeOrder'),
]
