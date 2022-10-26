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
    	return "{} {} ".format(self.id, self.title)    
    
 
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null = True)
    quantity = models.IntegerField(null=True)
    selling_price = models.IntegerField(null=True)
    is_active  = models.BooleanField(null = True, default = True)
    def __str__(self):
    	return "{} {} ".format(self.id, self.product)   
    
    
    
class  order(models.Model):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    product = models.ManyToManyField(cart)
    order_status = models.BooleanField(default= True) #User received the product it returns True --> false mean bending
    def __str__(self):
    	return "{} {} ".format(self.id, self.order_user, self.order_status)
    
    
