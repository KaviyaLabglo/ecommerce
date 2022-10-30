from django.urls import path
from myapp import views
from .views import *

urlpatterns = [
    
  
    #path('',login_page, name= 'login'),
    path('view_page/', views.show_products, name='viewpage'),
    path('home/', product_list.as_view(), name='home'),
    
    path('co/<int:id>/', views.cart_form, name='cf'),
    
    path('add/<int:id>/', views.add, name = 'add'),
    path('del_mycart/<int:id>/', views.cart_del, name='cart_delete'),
    #path('logout/',views.logout_user, name='logout'),

    path('mycart/', views.my_cart, name='mycart'),
    path('order/<int:id>/', views.order_table, name='order'),
    path('history/', views.order_history, name = 'history'),
    path('orderdel/<int:id>/', views.order_del, name='order_del'),
    
    path('wishlist/<int:id>/', views.add_wish, name="wishlist"),
    path('my_wishlist/', views.my_wishlist, name='mwl'),
    path('del_wl/<int:id>/', views.wishlist_del, name='delwl'),
    path('wlf/<int:id>/', views.cart_form, name='wlf'),
    
    
    path('shipping/<int:id>/', views.shipping, name='shipping'),
    
    ]
  

