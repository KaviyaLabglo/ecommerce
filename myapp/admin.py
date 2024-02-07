from django.contrib.sessions.models import Session
from django.contrib import admin
from myapp.models import *


class S(admin.ModelAdmin):
    # fields = ('id', 'brand', 'image', 'price',
    #               'availability', 'color', 'created_on')
    fieldsets = (
        (None, {
            'fields': (

                'brand',
                'image',

                'availability',
                'color',
                'price'
            )
        }),
    )


admin.site.register(product, S)


class add(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'quantity',
                    'selling_price', 'is_active', 'created_on', 'updated_quantity')
    list_display_links = ('selling_price',)
    list_editable = ('quantity', 'user',)
    list_filter = ('id', )
    search_fields = ('id', 'user')


admin.site.register(cart, add)


class ord(admin.ModelAdmin):
    list_display = ('id', 'order_user', 'order_status',  
                    'created_on')


admin.site.register(order, ord)


class a(admin.ModelAdmin):
    list_display = ('id', 'user1', 'product1', 'price',
                    'is_active1', 'created_on')


admin.site.register(wishlist, a)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)



class BranndAdmin(admin.ModelAdmin):
    list_display = ('id', )

admin.site.register(Brand, BranndAdmin)