from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class product(models.Model):
    brand = models.TextField(max_length = 100)
    image = models.ImageField(null = True, upload_to = 'image/')
    title = models.CharField(max_length = 100)
    price = models.IntegerField(blank = True,null = True)
    availability = models.BooleanField(default = False)
    color = models.CharField(max_length=200)
    def __str__(self):
    	return "{} ".format(self.id)    
    
 
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null = True)
    quantity = models.IntegerField(null=True, default = 1)
    selling_price = models.IntegerField(null=True)
    is_active  = models.BooleanField(null = True, default = True)
    addcart_by = models.CharField(max_length = 200, null = True)
    
    
    
class  order(models.Model):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ManyToManyField(cart)
    order_status = models.BooleanField(default= True) #User received the product it returns True --> false mean bending
   
    def __str__(self):
    	return "{} {} ".format(self.id, self.order_user, self.order_status)
    
class wishlist(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product1 = models.ForeignKey(product, on_delete=models.CASCADE, null = True)
    price = models.IntegerField(null=True)
    is_active1  = models.BooleanField(null = True, default = True)
    
   
    
