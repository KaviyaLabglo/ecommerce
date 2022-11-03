from django.contrib import admin
from myapp.models import *


class S(admin.ModelAdmin):
    #fields = ('id', 'brand', 'image', 'price',
     #               'availability', 'color', 'created_on')
    fieldsets = (
        (None,{
            'fields' : (
                  
                  'brand', 
                  'image',
                  
                    'availability',
                    'color',
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
    list_display = ('id', 'order_user', 'order_status',  'shipping_address',
                    'created_on', 'total_product_price', 'total_tax', 'total_order_value')


admin.site.register(order, ord)


class a(admin.ModelAdmin):
    list_display = ('id', 'user1', 'product1', 'price',
                    'is_active1', 'created_on')


admin.site.register(wishlist, a)

'''class b(admin.ModelAdmin):
    fields = ('id','brand_name', 'brand_logo', 'year', 'founder')
    
admin.site.register(Brand,b)'''


# lookup_field
'''
GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "myapp": {
        "order": ("order_user", "product",)
    }
}

class orderOptions(admin.ModelAdmin):
    # define the raw_id_fields
    raw_id_fields = ('order_user','product',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['order_user'],
        'm2m': ['product'],
    }'''


'''class cartInline(admin.TabularInline):
    model = cart
    fk_name = "product"
    

class productAdmin(admin.ModelAdmin):
    inlines = [
        cartInline,
    ]
    '''
