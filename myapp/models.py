from distutils.command.upload import upload
from operator import mod
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
FAILED = 0
SUCCESS = 1
PENDING = 2
ORDER_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (PENDING, 'Pending'),
    (FAILED, 'Cancel')
)  

class TimeStampModel(models.Model):
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True   
        
    
class Brand(TimeStampModel):
    brand_name = models.CharField(max_length = 200)
    brand_logo = models.ImageField(upload_to = 'image/')
    year = models.IntegerField()
    founder = models.CharField(max_length = 200)
    def __str__(self):
    	return "{}".format(self.brand_name)
     
class product(TimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'image/')
    title = models.TextField(max_length = 200)
    price = models.IntegerField()
    availability = models.BooleanField(default = False)
    color = models.CharField(max_length=200)
    def __str__(self):
    	return "{} ".format(self.id)    
    
 
class cart(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    updated_quantity = models.IntegerField(null = True)
    selling_price = models.IntegerField()
    is_active  = models.BooleanField(default = True)
    addcart_by = models.CharField(max_length = 200)
    def __str__(self):
    	return "{} ".format(self.id)
    
    
    
class  order(TimeStampModel):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(cart)
    order_status = models.IntegerField(default= 2,choices = ORDER_STATUS_CHOICES) #User received the product it returns True --> false mean bending
    shipping_address = models.TextField(max_length = 200)
    total_product_price = models.IntegerField()
    total_tax =  models.IntegerField()
    total_order_value =  models.IntegerField()
    
    @staticmethod
    def autocomplete_search_fields():
        return ("order_user", "product",)
   
    def __str__(self):
    	return "{} {} ".format(self.id, self.order_user, self.order_status)
    
class wishlist(TimeStampModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    product1 = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active1  = models.BooleanField(default = True)
    def __str__(self):
    	return "{} ".format(self.id)
   
    
   
    
