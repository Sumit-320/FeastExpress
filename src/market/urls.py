from django.urls import path
from . import views
urlpatterns=[
    path('',views.market,name='market'),
    path('<slug:vendor_slug>/',views.vendorDetail,name='vendorDetail'),
    path('add_to_cart/<int:food_id>/',views.addToCart,name='addToCart'),
    path('decrease_cart/<int:food_id>/',views.decreaseCart,name='decreaseCart'),
    path('delete_cart/<int:cart_id>/',views.deleteCart,name='deleteCart')
]