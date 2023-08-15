from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from shop.models import *

from sparklesapp.forms import ProductForm

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
                    return HttpResponseRedirect('/')
                else:
                    raise Exception()
    

def homepage(request):
    return render(request, "user/homepage.html")

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
    context["orders"] = Order.objects.all()
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
                                             "category" : product.category})
    
    return render(request, "seller/add_product.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def user_details(request):
    id = request.GET.get('id', None)

    user = User.objects.filter(id=id).first()
    context = dict()
    
    context["user"] = user
    
    return render(request, "seller/user_details.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def admin_logout(request):
    logout(request)
    return render(request, "seller/logout.html")
