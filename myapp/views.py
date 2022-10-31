import re
from django.views.generic.list import ListView

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.style import available
from myapp.models import *
from django.template import loader

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.db.models import Min, Max, Count, Avg, Sum
from django.db.models import Q, F
from datetime import datetime

from django.contrib.auth.decorators import login_required

 
class product_list(ListView):
    model = product
    template_name = 'app.html'
    success_url = 'home'
    def get_queryset(self):
        a = product.objects.filter(availability = True)
        return a 
    def get_context_data(self, **kwargs):
        s=super().get_context_data(**kwargs)
        wishlist_items = wishlist.objects.filter(user1 = self.request.user.id).values('product1')
        List = []
    
        for i in wishlist_items:
            List.append(i['product1'])
        s['content'] =List
        print("kuygruf feudfsgsefh ",s)
        return s

def show_products(request):
     search_content = request.POST.get('content')
     print(search_content)
     show = product.objects.filter( Q(availability = True) & Q(brand__brand_name__istartswith= search_content) | Q(title__istartswith =  search_content))
     print(show)
     wishlist_items = wishlist.objects.filter(user1 = request.user.id).values('product1')
     List = []
    
     for i in wishlist_items:
        List.append(i['product1'])
    
     content = {'i':List}
     return render(request, 'product.html', {'form': show, 'wl':content})
     
     
    
def cart_form(request, id):
    select_item = product.objects.filter(id=id)
    return render(request, 'cart.html',{'object_list':select_item})
    
    
@login_required       
def add(request, id):
   
    if request.method == 'POST':
        quan_tity = request.POST.get('quan')

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
    print(request.method)
    if request.method =='POST':
        dele = cart.objects.get(id=id).delete()
        return redirect('mycart')
    
    
@login_required    
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
    print(request.method)
    
    if request.method == 'POST':
        address = request.POST.get('ad')
        city = request.POST.get('ci')
        state = request.POST.get('st')
        zipcode = request.POST.get('zi')
        add = address+','+city+','+state+','+zipcode
        current_user = request.user
        get_user = User.objects.get(username= request.user)
        total_price = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
        print(total_price)
        tax = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tax = Sum(F('selling_price') * F('quantity')) * 0.18)
        print(tax)
        if tax['tax']:
            car = cart.objects.filter(Q(user_id = current_user.id) & Q(is_active = True))       
            s = order.objects.create(order_user =User.objects.get(id = current_user.id), shipping_address = add, total_product_price = total_price['tot'],  total_tax = tax['tax'], total_order_value =total_price['tot'] + tax['tax'] )
            s.product.add(*car)
            cart.objects.filter(user_id = id).update(is_active=False)
            
            ret1 = order.objects.filter(order_user = current_user.id).values('id').last()
            print(ret1['id'])
            ret = order.objects.filter(id = ret1['id']).values('product__product_id__image')

            print(ret)
            print(tax)
        
            return render(request, 'order.html',{'form':ret, 'sum':total_price, 'Tax':tax})
        else:
            return redirect('home')
        
@login_required
def order_history(request):
    current_user = request.user
    sel = order.objects.filter(order_user = current_user).values()
    print(sel)
    #values('product__product_id__image', 'order_user', 'id', 'product__selling_price', 'product__quantity', 'created_on', 'total_order_value', 'product__id')
    return render(request, 'history.html', {'sel': sel})
def order_del(request,id):
    if request.method == 'POST':
        dele = cart.objects.get(id = id).delete()
        print(dele)
        return redirect('history')
    
       
@login_required  
def add_wish(request, id):
    if request.method == 'POST':
        product_id = int(id)
        get_price = product.objects.get(id =id)
        price = get_price.price
        a = wishlist.objects.filter (user1 = request.user).values('product1')
        print(a)
        usre_id = User.objects.get(username= request.user)
        if a :
            print('Do not save')
            pass
        else:
            p = wishlist(user1 = User.objects.get(id= usre_id.id), product1 = product.objects.get(id =id),  price = price)
            p.save()
    
    return redirect('mwl')
   
    
@login_required
def my_wishlist(request):
    current_user = request.user
    sel = wishlist.objects.filter(user1 = current_user.id).values('product1__image', 'product1__price', 'id', 'product1__id')
    return render(request, 'wishlistview.html', {'wish_list': sel})
      

    
def wishlist_del(request,id):
    if request.method == 'POST':
        dele = wishlist.objects.get(id=id).delete()
        return redirect('mwl')

def wl_form(request, id):
    print("HII")
    select_item = product.objects.filter(id=id)
    return render(request, 'cart.html',{'object_list':select_item})
         
  
def shipping(request, id):
    print(request.method)
    print(1)
    if request.method == "POST":
        print(2)
        a = cart.objects.filter(Q(user = id) & Q(is_active = True)).values('product_id', 'product_id__image', 'selling_price', 'user')
        print(a)
        current_user = request.user
    
        get_user = User.objects.get(username= request.user)
        total_price = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tot = Sum(F('selling_price') * F('quantity')))
        tax = cart.objects.filter(Q(user_id= get_user.id) & Q(is_active = True)).aggregate(tax = Sum(F('selling_price') * F('quantity')) * 0.18)
        return render(request, 'shipping.html',{'form':a, 'sum':total_price, 'Tax':tax})
    
  
from django.shortcuts import redirect, render
from django.urls import reverse
from myapp.form import CustomUserCreationForm


def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("login")) 

    
    
    
    
   
