from django.urls import path
from myapp import views
from .views import *

urlpatterns = [
    
  
    #path('',login_page, name= 'login'),
    path('view_page/', views.show_products, name='viewpage'),
    path('home/', product_list.as_view(), name='home'),
    
    path('co/<int:id>/', views.cart_form, name='cf'),
    
    path('add/<int:id>/', views.add, name = 'add'),
    #path('logout/',views.logout_user, name='logout'),

    path('mycart/', views.my_cart, name='mycart'),
    path('order/<int:id>/', views.order_table, name='order'),
    
    ]
  

