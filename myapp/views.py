from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate  , logout
from django.contrib import messages
from myapp.models import *
from django.template import loader
from django.db.models import Q
import datetime
import logging
logger = logging.getLogger(__name__)
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Min,Max,Count,Avg,Sum


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
        	username = form.cleaned_data.get('username')
        	password = form.cleaned_data.get('password')
        	user = authenticate(username=username, password=password)
        	if user is not None:
        	        login(request,user)
        	        messages.info(request, f"You are now logged in as {username}.")
        	        logger.warning('You are successfully logged at  '+str(datetime.datetime.now())+' hours!')
        	        return redirect('home')
        	else:
        	        messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    logger.error('Something went wrong!')
    return render(request, 'login.html', {'form': form})
    
    
    
def logout_user(request):
    logout(request)
    logger.warning('You Are Logged Out at '+str(datetime.datetime.now())+' hours!')
    return redirect('login')
    
class product_list(ListView):
    model = product
    template_name = 'app.html'
    success_url = 'home'

def show_products(request):
     pro = request.POST.get('content')
     show = product.objects.filter( Q(availability = True) & Q(brand__istartswith= pro)|Q(title__istartswith =  pro))
     return render(request, 'product.html', {'form': show})
     
     
    
def cart_form(request, id):
    select_item = product.objects.filter(id=id)
    return render(request, 'cart.html',{'object_list':select_item})
    
    
       
def add(request, id):
    quan_tity = request.GET.get('quan')
    product_id = int(id)
    get_price = product.objects.get(id =id)
    price = get_price.price
    total = price * int(quan_tity)
    usre_id = User.objects.get(username= request.user)
    a = cart(user = User.objects.get(id= usre_id.id), product = product.objects.get(id =id), quantity = quan_tity, selling_price = total) 
    
    cart_table = cart.objects.filter(user_id = usre_id)
    print(cart_table)
    a.save() 
    total_price = cart.objects.filter(user_id= usre_id.id).aggregate(Sum('selling_price'))
    return render(request, 'carttable.html',{'form':cart_table,'Sum':total_price})

     
def my_cart(request):
    usre_id = User.objects.get(username= request.user)
    cart_table = cart.objects.filter(user_id = usre_id.id).values('product_id__image', 'product_id', 'selling_price','id')
    get_user = User.objects.get(username= request.user)
    total_price = cart.objects.filter(user_id= get_user.id).aggregate(Sum('selling_price'))
    print( cart_table)
    
    return render(request, 'carttable.html',{'form':cart_table, 'Sum':total_price})
       
def order(request,id):
    user_name = User.objects.get(username= request.user)
    user_id = User.objects.get(id = user_name.id)
    print(user_id.id)
    car = cart.objects.get(user_id = user_id)
    print(car)
    s = order(user= User.objects.get(id= user_name.id), product = car.product_id)
    #s.save()
    ret = order.objects.all()
    return render(request, 'carttable.html',{'form':ret})

    
       


     
     
     

    
         
   
   
