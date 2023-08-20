from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from shop.models import *
from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib import messages
import re
from django.template import loader

from sparklesapp.forms import *

# Group check 

def is_buyer(user):
    return user.groups.filter(name='Buyer').exists()

def is_seller(user):
    return user.groups.filter(name='Seller').exists()

# Create your views here.

def user_login(request):
    return render(request, "user/user_login.html")

def admin_login(request):
    return render(request, "seller/seller_login.html")

def page_login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if is_seller(user):
                    return HttpResponseRedirect('/dashboard')
                elif is_buyer(user):
                    print("BUYER")
                    return HttpResponseRedirect('/')
                else:
                    raise Exception("No role assigned to user please assign seller or buyer role.")
        else:
            return render(request, "user/user_login.html", {'error_msg': "Invalid username or password"})



@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def dashboard(request):
    return render(request, "seller/dashboard.html")

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def manage_users(request):
    context= dict()
    context["users"] = User.objects.all()
    return render(request, "seller/users_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def manage_products(request):
    context= dict()
    context["products"] = Product.objects.all()
    
    return render(request, "seller/products_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def manage_orders(request):
    context= dict()
    context["orders"] = Order.objects.filter(paid=True).all()
    return render(request, "seller/orders_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def add_product(request):
    if request.method == "POST":
        form_data = ProductForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            product = form_data.save(commit=False)
            product.image = form_data.cleaned_data["image"]
            product.save()
            return redirect("/products")
    context = dict()
    context["form"] = ProductForm
    
    return render(request, "seller/add_product.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def product_details(request):
    print("ITS ANYKIND METHOD")
    id = request.GET.get('id', None)

    product = Product.objects.filter(id=id).first()
    
    if request.method == "POST":
        form_data = ProductForm(data=request.POST, files=request.FILES)
        print(form_data.errors)
        if form_data.is_valid():
            # product = form_data.save(commit=False)
            print(form_data.cleaned_data["name"])
            product.name = form_data.cleaned_data["name"]
            product.quantity = form_data.cleaned_data["quantity"]
            img =form_data.cleaned_data["image"]
            if img:
                product.image = form_data.cleaned_data["image"]
            product.price = form_data.cleaned_data["price"]
            product.description = form_data.cleaned_data["description"]
            product.category = form_data.cleaned_data["category"]
            product.brand = form_data.cleaned_data["brand"]
            product.save()
            print("ITS POST METHOD")
            return redirect("/products")
    if id is None:
        return redirect("/products")
    context = dict()
    
    context["form"] = ProductForm(initial = {"id": id,
                                            "name" : product.name,
                                             "quantity" : product.quantity,
                                             "image" : product.image,
                                             "price" : product.price,
                                             "description" : product.description,
                                             "category" : product.category,
                                             "brand" : product.brand})
    
    return render(request, "seller/add_product.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def user_details(request):
    id = request.GET.get('id', None)

    user = User.objects.filter(id=id).first()
    context = dict()
    
    context["user"] = user
    context["orders"] = Order.objects.filter(user = user, paid=True).all()
    return render(request, "seller/user_details.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def admin_logout(request):
    logout(request)
    return render(request, "seller/logout.html")

def signout(request):
    logout(request)
    return redirect("/")


def homepage(request):
    context = dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    latest_products = Product.objects.all()
    context['latest_products'] =latest_products[len(latest_products)-3:]
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            
            if cookie == -1:
                break
            index+=1
        
        context['shopping_cart_items'] = index

    return render(request, "user/homepage.html", context=context)


def categories(request):
    context = dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    id = request.GET.get('id', None)
    category = Category.objects.filter(id=id).first()
    products = Product.objects.filter(category__id=id).all()
    context['products'] = products
    context['title'] = f"Products from the category {category.name}"
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1
        
        context['shopping_cart_items'] = index
    return render(request, "user/product_list.html", context=context)

def brands(request):
    context = dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    id = request.GET.get('id', None)
    brand = Brand.objects.filter(id=id).first()
    products = Product.objects.filter(brand__id=id).all()
    context['products'] = products
    context['title'] = f"Products from the brand {brand.name}"
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1
        
        context['shopping_cart_items'] = index
    return render(request, "user/product_list.html", context=context)

def product(request):
    context=dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    id = request.GET.get('id', None)
    product = Product.objects.filter(id=id).first()
    context['product'] = product
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1
        
        context['shopping_cart_items'] = index
    return render(request, "user/product_details.html", context=context)

def register(request):
    logout(request)
    context = dict()
    context['form'] = RegisterForm
    if request.method == "POST":
        form = RegisterForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            context['error_msg'] = "Unsuccessful registration. Invalid information."
    return render(request, "user/user_register.html", context)

def add_to_cart(request):
    
    id = request.GET.get('id', None)
    qty = request.GET.get('qty', None)
    if isinstance(request.user,AnonymousUser):
        print("HERE")
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1
        response = HttpResponse()
        response.set_cookie('sc'+str(index), 1)
        
        response.set_cookie('sc'+str(index)+"_id", id)
        
        response.set_cookie('sc'+str(index)+"_qty", qty)
    else:
        shopping_cart_item = ShoppingCart(user = request.user,
                                            product = Product.objects.filter(id=id).first(),
                                            quantity=qty)
        shopping_cart_item.save()
    
    return response
def update_shopping_cart(request):
    
    id = request.GET.get('id', None)
    qty = request.GET.get('qty', None)
    response = HttpResponse()
    if isinstance(request.user,AnonymousUser):
        response.set_cookie('sc'+str(id)+"_qty", qty)
    else:

        shopping_cart_item = ShoppingCart.objects.filter(id=id).first()
        shopping_cart_item.quantity = qty
        shopping_cart_item.save()
    
    return response
def shopping_cart(request):
    context=dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    scitems = []
    if isinstance(request.user, AnonymousUser):
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            cookie_id = request.COOKIES.get('sc'+ str(index)+"_id", -1)
            
            cookie_qty = request.COOKIES.get('sc'+ str(index)+"_qty", -1)
            
            
            if cookie == -1:
                break
            scitems.append(ShoppingCart(id=index, product = Product.objects.filter(id=cookie_id).first(),
                                         quantity=cookie_qty))
            index+=1
    else:
        scitems = ShoppingCart.objects.filter(user_id = request.user.id)

    context['products'] = scitems
    context['total_price'] = sum([int(item.product.price)*int(item.quantity) for item in scitems])
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1
    
        context['shopping_cart_items'] = index
        
    return render(request, "user/shopping_cart.html", context)

def delete_sc_product(request):
    id = request.GET.get('id', None)
    response = HttpResponse()
    if isinstance(request.user,AnonymousUser):
        print(id)
        index = int(id)
        while(True):
            cookie_val = request.COOKIES.get('sc'+ str(index+1), -1)
            if cookie_val == -1:
                break
            response.set_cookie('sc'+str(index), cookie_val)
            response.set_cookie('sc'+str(index)+"_id", request.COOKIES.get('sc'+ str(index+1) +"_id"))         
            response.set_cookie('sc'+str(index)+"_qty", request.COOKIES.get('sc'+ str(index+1) + "_qty"))
            index+=1

        response.delete_cookie('sc'+str(index))
        response.delete_cookie('sc'+str(index)+"_id")
        response.delete_cookie('sc'+str(index)+"_qty")
    else:
        scitem = ShoppingCart.objects.filter(id=id)
        scitem.delete()

    return response

def checkout(request):
    context = dict()
    context['form'] = OrderForm
    if request.method == "POST":
        form_data = OrderForm(data=request.POST, files=request.FILES)
        
        if form_data.is_valid():
            order = form_data.save(commit=False)
            order.total = 0
            order.paid = False
            if isinstance(request.user,AnonymousUser):
                guest_user = User.objects.filter(username="GuestUser").first()
                order.user = guest_user
            else:
                order.user = request.user
                context['payment_options'] = CreditCard.objects.filter(user=request.user).all()
            order.save()
            context['order'] = order

            return render(request, "user/payment_option.html", context)
    return render(request, "user/order_info.html",context= context)
def add_order_items_cookie(orderId, request):
    index = 0
    total = 0
    order_items = []
    while(True):
        cookie = request.COOKIES.get('sc'+ str(index), -1)
        
        if cookie == -1:
            break
        order_item = OrderItem(product = Product.objects.filter(id=request.COOKIES.get('sc'+ str(index) + "_id", -1)).first(),
                               quantity = request.COOKIES.get('sc'+ str(index)+"_qty", -1),
                               order = Order.objects.filter(id=orderId).first())
        total += order_item.product.price * order_item.quantity
        order_item.save()
        order_items.append(order_item)
        index+=1
    return total,order_items
def add_order_items_db(orderId, user):
    index = 0
    total = 0
    order_items = []
    sc_items = ShoppingCart.objects.filter(user_id=user.id).all()
    for item in sc_items:
        order_item = OrderItem(product = Product.objects.filter(id=item.product.id).first(),
                               quantity = item.quantity,
                               order = Order.objects.filter(id=orderId).first())
        total += order_item.product.price * order_item.quantity

        order_item.save()
        order_items.append(order_item)
        index+=1
    return total,order_items
def payment_info(request):
    context = dict()
    
    if request.method=="POST":
        form_data = PaymentForm(data=request.POST, files=request.FILES)
        id = request.GET.get('id', None)
        order = Order.objects.filter(id=id).first()
        if form_data.is_valid():
            creditcard = form_data.save(commit=False)
            order_items = []
            total=0
            if isinstance(request.user,AnonymousUser):
                guest_user = User.objects.filter(username="GuestUser").first()
                # credi.user = guest_user
                order.user = guest_user

                total,order_items =add_order_items_cookie(id, request)    
            else:
                creditcard.user = request.user
                total,order_items = add_order_items_db(id, request.user)
                order.user = request.user
            order.total = total
            order.paid = True
            order.save()
            context['order_items'] = order_items
            return render(request, "user/payment_succesful.html", context)
        else:
            context['error_msg'] = "Invalid information"
    context['form'] = PaymentForm

    return render(request, "user/payment_form.html", context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def order_details(request):
    id = request.GET.get('id', None)
    context = dict()
    context['order'] = Order.objects.filter(id=id, paid=True).first()
    context['order_items'] = OrderItem.objects.filter(order = context["order"]).all()
    return render(request, "seller/order_details.html", context)   
