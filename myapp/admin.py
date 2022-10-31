from django.contrib import admin
from myapp.models import *

class S(admin.ModelAdmin):
    list_display = ('id','brand','image','price',  'availability', 'color', 'created_on')
admin.site.register(product,S)

class add(admin.ModelAdmin):
    list_display = ('id','user', 'product_id', 'quantity','selling_price', 'is_active', 'created_on')
admin.site.register(cart,add)

class ord(admin.ModelAdmin):
    list_display = ('id','order_user', 'order_status',  'shipping_address', 'created_on', 'total_product_price', 'total_tax', 'total_order_value')
admin.site.register(order,ord)

class a(admin.ModelAdmin):
    list_display = ('id','user1', 'product1','price', 'is_active1', 'created_on' )
admin.site.register(wishlist,a)

class b(admin.ModelAdmin):
    list_display = ('id','brand_name', 'brand_logo', 'year', 'founder')
admin.site.register(Brand,b)
