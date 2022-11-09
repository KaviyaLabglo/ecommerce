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
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


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
    select_item = product.objects.filter(id=id1)
    return render(request, 'cart.html', {'object_list': select_item})


@login_required
def cart_add(request, id):
    if request.method == 'POST':
        quan_tity = request.POST.get('quan')
        get_price = product.objects.get(id=id)
        price = get_price.price
        usre_id = User.objects.get(username=request.user)
        a = cart(user=User.objects.get(id=usre_id.id), product=product.objects.get(
            id=id), quantity=quan_tity, selling_price=price, addcart_by=request.user)
        #cart_table = cart.objects.filter(user_id = usre_id)
        a.save()
        return redirect('mycart')
        '''total_price = cart.objects.filter(Q(user_id=usre_id.id) & Q(
            is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
        tax = cart.objects.filter(Q(user_id=usre_id.id) & Q(is_active=True)).aggregate(
            tot=Sum(F('selling_price') * F('quantity')) * 0.18)
        '''
        # return render(request, 'carttable.html',{'form':cart_table,'Sum':total_price, 'Tax':tax})


@user_passes_test(lambda user: user.id)
def cart_update(request, id):
    if request.method == 'POST':
        qn = request.POST.get('qn')
        cart.objects.filter(product=id).update(quantity=int(qn))
        return redirect('mycart')


@user_passes_test(lambda user: user.id)
def cart_del(request, id):
    if request.method == 'POST':
        cart.objects.get(id=id).delete()
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
    key = settings.STRIPE_PUBLISHABLE_KEY
    print(key)
    return render(request, 'carttable.html', {'form': cart_table, 'Sum': total_price, 'pass_id': d, 'Tax': tax, 'total': to, 'key': key})


stripe.api_key = settings.STRIPE_SECRET_KEY


@user_passes_test(lambda user: user.id)
def order_table(request, id):
    print("Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
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
            sum_total = total_price['tot'] + tax['tax']
            print(sum_total)
            a = stripe.PaymentIntent.create(amount=int(
                sum_total), currency="usd", payment_method_types=["card"])
           
            print(a['client_secret'])
            print('ID', a['id'])
            return render(request, 'order.html', {'form': ret, 'sum': total_price, 'Tax': tax})
        else:
            return redirect('home')
#charge = stripe.Charge.create(amount = 800, currency = 'inr', description  = "Payment Gateway", source= request.POST['stripeToken'])#


@login_required
def order_history(request):
    current_user = request.user
    sel = order.objects.filter(order_user=current_user).values('product__product_id__image', 'order_user',
                                                               'id', 'product__id')
    print(sel)
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


@user_passes_test(lambda user: user.id)
def order_del(request, id1, id2):
    if request.method == 'POST':
        current_user = request.user.id
        a = cart.objects.get(id=id1)
        b = order.objects.get(id=id2)
        b.product.remove(a)

        pr = order.objects.filter(Q(order_user=current_user) & Q(id=id2)).values(
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





def register(request):
    if request.method == "GET":
        return render(request, "registration/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("login"))
        else:
            form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


class productapi(ListView):
    model = product

    def render_to_response(self, context, **kwargs):
        qs = self.get_queryset()
        queryset = serializers.serialize('json', qs, indent=4)
        return HttpResponse(queryset, content_type='application/json')


class cartapi(ListView):
    model = cart

    def render_to_response(self, context, **kwargs):
        qs = self.get_queryset()
        filter_qs = qs.filter(Q(user=self.request.user) & Q(is_active=True))
        queryset = serializers.serialize('json', filter_qs, indent=4)
        return HttpResponse(queryset, content_type='application/json')


class orderapi(ListView):
    model = order

    def render_to_response(self, context, **kwargs):
        qs = self.get_queryset()
        filter_qs = qs.filter(
            Q(order_user=self.request.user) & Q(order_status=2))
        queryset = serializers.serialize('json', filter_qs, indent=4)
        return HttpResponse(queryset, content_type='application/json')


class orderapi(ListView):
    model = order

    def render_to_response(self, context, **kwargs):
        qs = self.get_queryset()
        filter_qs = qs.filter(
            Q(order_user=self.request.user) & Q(order_status=2))
        queryset = serializers.serialize('json', filter_qs, indent=4)
        return HttpResponse(queryset, content_type='application/json')


class searchapi(ListView):
    model = product

    def render_to_response(self, context, **kwargs):
        search_content = self.request.GET.get('se')
        qs = self.get_queryset()
        filter_qs = qs.filter(Q(availability=True) & Q(
            brand__brand_name__istartswith=search_content) | Q(title__istartswith=search_content))
        queryset = serializers.serialize('json', filter_qs, indent=4)
        return JsonResponse(json.loads(queryset), safe=False)


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_43307a15a7637563e099e6037008b2c2b674cf126fc8ab425e29bede7bd24512'



@csrf_exempt
def my_webhook_view(request):
    payload = request.body.decode('utf-8')
    a = json.loads(payload)
    print(payload)
    new = a["data"]["object"]["id"]
    print(new)
    dic = {
        "Succcess":a["type"] == "checkout.session.completed",
        "Failure":a["type"] == "charge.failed",
        "Payment_intend":a["type"] ==  "payment_intent.payment_failed", 
    }
    print(dic)
    
    if dic["Failure"]:
        print("Failed payment")
    if a["type"] == "checkout.session.completed":
            order_id = a['data']['object']["metadata"]["order_id"]
            email = a['data']['object']["customer_details"][ "email"]
            amount = a['data']['object']["amount_total"]
            order.objects.filter(id = order_id).update(order_status = 1, total_order_amount = amount)
            x = payment.objects.filter(transaction_id = a["data"]["object"]["id"]).update(paid_status = True, transaction_id = new, email = email, amount = amount)
     
    return HttpResponse("Webhook Success", status = 200)

    
def success(request):
    return render(request, 'success.html')
    


@csrf_exempt
def create_checkout_session(request):
    current_user = request.user
    domain_url = 'http://localhost:8000/myapp/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    get_user = User.objects.get(username=request.user)
    total_price = cart.objects.filter(Q(user_id=get_user.id) & Q(
             is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
    tax = cart.objects.filter(Q(user_id=get_user.id) & Q(is_active=True)).aggregate(
    tot=Sum(F('selling_price') * F('quantity'))*0.18)
    
    if tax['tot']:
        total = total_price['tot'] + tax['tot']  
       
    cart_product = cart.objects.filter(
                Q(user_id=current_user.id) & Q(is_active=True))
     
    
    o = order.objects.create(order_status = 2, order_user_id = User.objects.get(id = current_user.id).id, total_order_amount = 0)
    o.product.add(*cart_product)
    cart.objects.filter()
    
    cart_product.update(is_active = False)
   
    
    checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
        
            success_url=domain_url +'success/',
            cancel_url=domain_url + 'cancelled/',
            payment_method_types=['card'],
            line_items=[
                    {
                        'price_data': {
                            'unit_amount': int(total),
                            'currency': 'inr',
                            'product_data': {'name': 'Mobile'},
                        },
                        'quantity': 1,
                    }
                ],
            
            metadata = {"order_id": o.id},
            mode='payment',
    )
    pay_create = payment.objects.create(email = "aaa@gmail.com", amount =0 , paid_status =False, transaction_id =checkout_session["id"] ,order_id = o.id)
   
    print(checkout_session)
    return redirect(checkout_session.url, code = 303)
        
        
        
