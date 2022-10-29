from django.db.models import Min, Max, Count, Avg, Sum
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from myapp.models import *
from django.template import loader
from django.db.models import Q, F
from datetime import datetime
import logging
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)
 
class product_list(ListView):
    model = product
    template_name = 'app.html'
    success_url = 'home'

def show_products(request):
     pro = request.POST.get('content')
     show = product.objects.filter( Q(availability = True) & Q(brand__istartswith= pro)|Q(title__istartswith =  pro))
     w = wishlist.objects.filter(user1 = request.user.id).values('product1')
     a = []
     for i in w:
        a.append(i['product1'])

     d = {'i':a}
     return render(request, 'product.html', {'form': show, 'wl':d})
     
     
    
def cart_form(request, id):
    select_item = product.objects.filter(id=id)
    return render(request, 'cart.html',{'object_list':select_item})
    
    
       
def add(request, id):
    quan_tity = request.GET.get('quan')
    product_id = int(id)
    get_price = product.objects.get(id =id)
    price = get_price.price
    
    usre_id = User.objects.get(username= request.user)
    a = cart(user = User.objects.get(id= usre_id.id), product = product.objects.get(id =id), quantity = quan_tity, selling_price = price, addcart_by = request.user) 
    cart_table = cart.objects.filter(user_id = usre_id)
    a.save() 
    total_price = cart.objects.filter(Q(user_id= usre_id.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id= usre_id.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity'))* 0.18)
    return redirect('mycart')
    #return render(request, 'carttable.html',{'form':cart_table,'Sum':total_price, 'Tax':tax})


def cart_del(request,id):
    dele = cart.objects.get(id=id).delete()
    return redirect('mycart')
    
    
     
def my_cart(request):
    current_user = request.user
    i_d = current_user.id
    d ={'ID' : i_d}
    usre_id = User.objects.get(username= request.user)
    cart_table = cart.objects.filter(user_id = usre_id.id).values('product_id__image', 'product_id', 'selling_price','id', 'user_id', 'is_active','quantity')
   
    get_user = User.objects.get(username= request.user)
    total_price = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity'))*0.18)

   
    if tax['tot']:
        total = total_price['tot'] + tax['tot']
        to = {'total': total}
    else :
         total = 0
         to = 0
    
    return render(request, 'carttable.html',{'form':cart_table, 'Sum':total_price, 'pass_id':d, 'Tax':tax,'total':to})
       
def order_table(request,id):
    print(id)
    address = request.GET.get('ad')
    city = request.GET.get('ci')
    state = request.GET.get('st')
    zipcode = request.GET.get('zi')
    add = address+','+city+','+state+','+zipcode
    current_user = request.user
    get_user = User.objects.get(username= request.user)
    total_price = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tax = Sum(F('selling_price') * F('quantity')) * 0.18)
    if tax['tax']:
        car = cart.objects.filter(Q(user_id = current_user.id) & Q(is_active = True))       
        s = order.objects.create(order_user =User.objects.get(id = current_user.id), shipping_address = add)
        s.product.add(*car)
        cart.objects.filter(user_id = id).update(is_active=False)
        ret = order.objects.filter(order_user = current_user.id)
        
        return render(request, 'order.html',{'form':ret, 'sum':total_price, 'Tax':tax})
    else:
        return redirect('home')
        

def order_history(request):
    current_user = request.user
    sel = order.objects.filter(order_user = current_user).values('product__product_id__image', 'order_user', 'id', 'product__selling_price', 'product__quantity', 'order_date')
    
    
    pr = order.objects.filter(order_user = current_user.id).values('product__selling_price', 'product__quantity')
    l = []
    for i in pr:
       l.append(i['product__selling_price']* i['product__quantity'])
    price = sum(l)
    tax = price * 0.18
    total = tax+price
    d = {'t':total}
    
    
    return render(request, 'history.html', {'sel': sel, 'T':d})
    
def order_del(request,id):
    dele = order.objects.get(id=id).delete()
    return redirect('history')
    
       

def wish(request, id):
    print(id)
    product_id = int(id)
    get_price = product.objects.get(id =id)
    price = get_price.price
    
    usre_id = User.objects.get(username= request.user)
    p = wishlist(user1 = User.objects.get(id= usre_id.id), product1 = product.objects.get(id =id),  price = price)
    p.save()
    
    return redirect('mwl')
   
    
   
def my_wishlist(request):
    current_user = request.user
    sel = wishlist.objects.filter(user1 = current_user.id).values('product1__image', 'product1__price', 'id', 'product1__id')
    print(sel)
    return render(request, 'wishlistview.html', {'wish_list': sel})
      

    
def wishlist_del(request,id):
    dele = wishlist.objects.get(id=id).delete()
    return redirect('mwl')

def wl_form(request, id):
    print("HII")
    select_item = product.objects.filter(id=id)
    return render(request, 'cart.html',{'object_list':select_item})
         
   
def shipping(request, id):
    a = cart.objects.filter(Q(user = id) & Q(is_active = True)).values('product_id', 'product_id__image', 'selling_price', 'user')
    print(a)
    current_user = request.user
    
    get_user = User.objects.get(username= request.user)
    total_price = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tax = Sum(F('selling_price') * F('quantity')) * 0.18)
    return render(request, 'shipping.html',{'form':a, 'sum':total_price, 'Tax':tax})
    
   

    
    
    
    
   
