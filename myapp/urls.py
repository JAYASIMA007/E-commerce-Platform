from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('product/<int:id>', views.ProductDetails.as_view(), name='productdetails'),
  path('mobile', views.Mobiles, name='mobile'),
  path('removecart', views.RemoveCart, name='removecart'),
  path('login', views.user_Login, name='login'),
  path('mobile/<slug:data>', views.Mobiles, name='mobiledetails'),
  path('registration', views.user_Regi, name='registration'),
  path('logout', views.user_Logout, name='logout'),
  path('changepassword', views.change_Password, name='changepassword'),
  path('profile', views.user_Profile, name='profile'),
  path('order', views.Ordered_Product, name='order'),
  path('payment', views.user_payment, name='payment'),
  path('addtocart', views.addToCart, name='addtocart'),
  path('showcart', views.showCarts, name='showcart'),
  path('addcartplus', views.cart_icon_plus, name='addcartplus'),
  path('addcartminus', views.cart_icon_minus, name='addcartminus'),
  path('address', views.user_Address, name='address'),
  path('checkout', views.Checkout, name='checkout'),
  path('mark-order-received/', views.mark_order_received, name='mark_order_received'),
  
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)