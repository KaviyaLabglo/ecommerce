from django.db import models
from django.contrib.auth.models import User
# Create your models here.
FAILED = 0
SUCCESS = 1
PENDING = 2
ORDER_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (PENDING, 'Pending'),
    (FAILED, 'FAILED')
)  

class TimeStampModel(models.Model):
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True   
        
class product(TimeStampModel):
    brand = models.TextField(max_length = 100)
    image = models.ImageField(null = True, upload_to = 'image/')
    title = models.CharField(max_length = 100)
    price = models.IntegerField(blank = True)
    availability = models.BooleanField(default = False)
    color = models.CharField(max_length=200)
    def __str__(self):
    	return "{} ".format(self.id)    
    
 
class cart(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null = True)
    quantity = models.IntegerField(null=True, default = 1)
    selling_price = models.IntegerField(null=True)
    is_active  = models.BooleanField(null = True, default = True)
    addcart_by = models.CharField(max_length = 200, null = True)
    def __str__(self):
    	return "{} ".format(self.product)
    
    
    
class  order(TimeStampModel):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ManyToManyField(cart)
    order_status = models.IntegerField(default= 2,choices = ORDER_STATUS_CHOICES) #User received the product it returns True --> false mean bending
    shipping_address = models.TextField(max_length = 200, null = True)
    total_product_price = models.IntegerField(null = True)
    total_tax =  models.IntegerField(null = True)
    total_order_value =  models.IntegerField(null = True)
   
    def __str__(self):
    	return "{} {} ".format(self.id, self.order_user, self.order_status)
    
class wishlist(TimeStampModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product1 = models.ForeignKey(product, on_delete=models.CASCADE, null = True)
    price = models.IntegerField(null=True)
    is_active1  = models.BooleanField(null = True, default = True)
    def __str__(self):
    	return "{} ".format(self.id)
   
    
   
    
