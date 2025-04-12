from django.urls import path
from . import views
urlpatterns = [
    path('place-order/',views.placeOrder,name='placeOrder'),
    path('payments/',views.payments,name='payments'),
    path('order_complete/',views.orderComplete,name='orderComplete')
]
