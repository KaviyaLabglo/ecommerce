from django.contrib import admin
from myapp.models import *

class S(admin.ModelAdmin):
    list_display = ('id','brand','image', 'title','price',  'availability', 'color')
admin.site.register(product,S)

class add(admin.ModelAdmin):
    list_display = ('id','user', 'product_id', 'quantity','selling_price', 'is_active')
admin.site.register(cart,add)

class ord(admin.ModelAdmin):
    list_display = ('id','order_user', 'order_status')
admin.site.register(order,ord)

class a(admin.ModelAdmin):
    list_display = ('id','user1', 'product1','price', 'is_active1', )
admin.site.register(wishlist,a)
