from myapp.form import CustomUserCreationForm
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from django.shortcuts import render, redirect
from matplotlib.style import context
from myapp.models import *

from django.contrib.auth.models import User
from django.contrib.auth import login

from django.db.models import Sum
from django.db.models import Q, F

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.contrib.auth.decorators import user_passes_test

class product_list(ListView):
    model = product
    template_name = 'app.html'
    success_url = 'home'

    def get_queryset(self):
        a = product.objects.filter(availability=True)
        return a

    def get_context_data(self, **kwargs):
        s = super().get_context_data(**kwargs)
        wishlist_items = wishlist.objects.filter(
            user1=self.request.user.id).values('product1', 'id')
        List = []
        for i in wishlist_items:
            List.append(i['product1'])
        s['content'] = List

        return s


def show_products(request):
    search_content = request.POST.get('content')
    
    
    show = product.objects.filter(Q(availability=True) & Q(
        brand__brand_name__istartswith=search_content) | Q(title__istartswith=search_content))
    wishlist_items = wishlist.objects.filter(
        user1=request.user.id).values('product1')
    List = []
    for i in wishlist_items:
        List.append(i['product1'])
    content = {'i': List}
    return render(request, 'product.html', {'form': show, 'wl': content})


@login_required
def cart_form(request, id1):
    print(id1)
    select_item = product.objects.filter(id=id1)
    return render(request, 'cart.html', {'object_list': select_item})


@login_required
def cart_add(request, id):
    if request.method == 'POST':
        quan_tity = request.POST.get('quan')
        product_id = int(id)
        get_price = product.objects.get(id=id)
        price = get_price.price
        usre_id = User.objects.get(username=request.user)
        a = cart(user=User.objects.get(id=usre_id.id), product=product.objects.get(
            id=id), quantity=quan_tity, selling_price=price, addcart_by=request.user)
        cart_table = cart.objects.filter(user_id=usre_id)
        a.save()
        total_price = cart.objects.filter(Q(user_id=usre_id.id) & Q(
            is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
        tax = cart.objects.filter(Q(user_id=usre_id.id) & Q(is_active=True)).aggregate(
            tot=Sum(F('selling_price') * F('quantity')) * 0.18)
        return redirect('mycart')
        # return render(request, 'carttable.html',{'form':cart_table,'Sum':total_price, 'Tax':tax})

@user_passes_test(lambda user:user.id)
def cart_update(request, id):
    print(request.user)
    if request.method == 'POST':
        qn = request.POST.get('qn')
        cart.objects.filter(product=id).update(quantity=int(qn))
        return redirect('mycart')

@user_passes_test(lambda user:user.id)
def cart_del(request, id):
    if request.method == 'POST':
        dele = cart.objects.get(id=id).delete()
        return redirect('mycart')


@login_required
def my_cart(request):
    current_user = request.user
    i_d = current_user.id
    d = {'ID': i_d}
    usre_id = User.objects.get(username=request.user)
    cart_table = cart.objects.filter(user_id=usre_id.id).values(
        'product_id__image', 'product_id', 'selling_price', 'id', 'user_id', 'is_active', 'quantity')
    get_user = User.objects.get(username=request.user)
    total_price = cart.objects.filter(Q(user_id=get_user.id) & Q(
        is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id=get_user.id) & Q(is_active=True)).aggregate(
        tot=Sum(F('selling_price') * F('quantity'))*0.18)
    if tax['tot']:
        total = total_price['tot'] + tax['tot']
        to = {'total': total}
    else:
        total = 0
        to = 0
    return render(request, 'carttable.html', {'form': cart_table, 'Sum': total_price, 'pass_id': d, 'Tax': tax, 'total': to})

@user_passes_test(lambda user:user.id)
def order_table(request, id):
    if request.method == 'POST':
        address = request.POST.get('ad')
        city = request.POST.get('ci')
        state = request.POST.get('st')
        zipcode = request.POST.get('zi')
        add = address+','+city+','+state+','+zipcode
        current_user = request.user
        get_user = User.objects.get(username=request.user)
        total_price = cart.objects.filter(Q(user_id=get_user.id) & Q(
            is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))

        tax = cart.objects.filter(Q(user_id=get_user.id) & Q(is_active=True)).aggregate(
            tax=Sum(F('selling_price') * F('quantity')) * 0.18)

        if tax['tax']:
            car = cart.objects.filter(
                Q(user_id=current_user.id) & Q(is_active=True))
            s = order.objects.create(order_user=User.objects.get(id=current_user.id), shipping_address=add,
                                     total_product_price=total_price['tot'],  total_tax=tax['tax'], total_order_value=total_price['tot'] + tax['tax'])
            s.product.add(*car)
            cart.objects.filter(user_id=id).update(is_active=False)

            ret1 = order.objects.filter(
                order_user=current_user.id).values('id').last()

            ret = order.objects.filter(id=ret1['id']).values(
                'product__product_id__image')

            return render(request, 'order.html', {'form': ret, 'sum': total_price, 'Tax': tax})
        else:
            return redirect('home')


@login_required
def order_history(request):
    current_user = request.user
    sel = order.objects.filter(order_user=current_user).values('product__product_id__image', 'order_user',
                                                               'id', 'product__selling_price', 'product__quantity', 'created_on', 'total_order_value', 'product__id')

   
    pr = order.objects.filter(order_user=current_user.id).values(
        'product__selling_price', 'product__quantity')
    l = []
    if pr:
        for i in pr:
            if i['product__selling_price'] is not None:
                l.append(i['product__selling_price'] * i['product__quantity'])
    else:
        l = [0, 0]

    price = sum(l)
    tax = price * 0.18
    total = tax+price
    d = {'t': total}
    return render(request, 'history.html', {'sel': sel, 'T': d})

@user_passes_test(lambda user:user.id)
def order_del(request, id1, id2):
    if request.method == 'POST':
        print(id1)
        print(id2)
        current_user = request.user.id
        a = cart.objects.get(id=id1)
        b = order.objects.get(id=id2)
        b.product.remove(a)

        pr = order.objects.filter(Q(order_user=current_user) & Q(id = id2)).values(
            'product__selling_price', 'product__quantity')
        l = []
        if pr:
            for i in pr:
                if i['product__selling_price'] is not None:
                    l.append(i['product__selling_price']
                             * i['product__quantity'])
        else:
            l = [0, 0]

        price = sum(l)
        tax = price * 0.18
        total = tax+price
        d = {'t': total}
        a = order.objects.filter(id=id2).update(
            total_order_value=total, total_product_price=price, total_tax=tax)
        if total == 0:
            order.objects.filter(id=id2).update(order_status=0)

        return redirect('history')


@login_required
def add_wish(request, id):
    if request.method == 'POST':
        get_price = product.objects.get(id=id)
        price = get_price.price
        a = wishlist.objects.filter(Q(user1=request.user) & Q(product1=id))
        usre_id = User.objects.get(username=request.user)
        if a:
            pass
        else:
            p = wishlist(user1=User.objects.get(id=usre_id.id),
                         product1=product.objects.get(id=id),  price=price)
            p.save()

    return redirect('home')


@login_required
def my_wishlist(request):
    current_user = request.user
    sel = wishlist.objects.filter(user1=current_user.id).values(
        'product1__image', 'product1__price', 'id', 'product1__id')
    return render(request, 'wishlistview.html', {'wish_list': sel})


def wishlist_del(request, id):
    if request.method == 'POST':
        dele = wishlist.objects.filter(Q(id=id) | Q(product1=id)).delete()
        return redirect('home')


def shipping(request, id):
    if request.method == "POST":
        a = cart.objects.filter(Q(user=id) & Q(is_active=True)).values(
            'product_id', 'product_id__image', 'selling_price', 'user')
        current_user = request.user
        get_user = User.objects.get(username=request.user)
        total_price = cart.objects.filter(Q(user_id=get_user.id) & Q(
            is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
        tax = cart.objects.filter(Q(user_id=get_user.id) & Q(is_active=True)).aggregate(
            tax=Sum(F('selling_price') * F('quantity')) * 0.18)
        return render(request, 'shipping.html', {'form': a, 'sum': total_price, 'Tax': tax})


def register(request):
    print(request.method)
    if request.method == "GET":
        return render(request, "registration/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(1)
        if form.is_valid():
            print('Hi')
            user = form.save()
            login(request, user)
            return redirect(reverse("login"))
        else:
            form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class productapi(ListView):
    model = product
    def render_to_response(self, context, **kwargs):
        print(context)
        print(self)
        qs  =self.get_queryset()
        queryset = serializers.serialize('json', qs, indent =4)
        return HttpResponse(queryset, content_type='application/json')

class cartapi(ListView):
    model = cart
    def render_to_response(self, context, **kwargs):
        print(context)
        qs  =self.get_queryset()
        filter_qs = qs.filter(Q(user = self.request.user) & Q(is_active = True))
        
        queryset = serializers.serialize('json', filter_qs, indent =4)
        return HttpResponse(queryset, content_type='application/json')
    
    
class orderapi(ListView):
    model = order
    def render_to_response(self, context, **kwargs):
        print(context)
        qs  =self.get_queryset()
        filter_qs = qs.filter(Q(order_user = self.request.user) & Q(order_status = 2))
        
        queryset = serializers.serialize('json', filter_qs, indent =4)
        return HttpResponse(queryset, content_type='application/json')
    
class orderapi(ListView):
    model = order
    def render_to_response(self, context, **kwargs):
        print(context)
        qs  = self.get_queryset()
        filter_qs = qs.filter(Q(order_user = self.request.user) & Q(order_status = 2))
        
        queryset = serializers.serialize('json', filter_qs, indent =4)
        return HttpResponse(queryset, content_type='application/json')
    
class searchapi(ListView):
    model = product
    def render_to_response(self, context, **kwargs):
        search_content = self.request.GET.get('se')
        '''self.request.session['my_values'] = search_content
        my_car = self.request.session.get('my_values')
        print(my_car)
        for key, value in self.request.session.items():
            print('{} => {}'.format(key, value))'''
        #del self.request.session['my_values']
        
        
        qs  =self.get_queryset()
        filter_qs = qs.filter(Q(availability=True) & Q(
        brand__brand_name__istartswith=search_content) | Q(title__istartswith=search_content))
        
        queryset = serializers.serialize('json', filter_qs, indent =4)
        return JsonResponse(json.loads(queryset), safe = False)
    
