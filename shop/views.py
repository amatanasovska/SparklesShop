import datetime
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
from django.db.models import Q

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


def get_most_visited_product_info():
    product = max(Product.objects.all(), key=lambda x: x.visits)
    times_bought = len(OrderItem.objects.filter(product=product))
    return {"product" : product, "times_bought": times_bought}

def get_number_users_in_interval(start, end):
    start_date = datetime.datetime.now()
    if start!=0:
        start_date = datetime.datetime.now() - datetime.timedelta(days = start)

    end_date = datetime.datetime.now()
    if end!=0:
        end_date = datetime.datetime.now() - datetime.timedelta(days = end)

    users = User.objects.filter(date_joined__gt=start_date, date_joined__lte=end_date)
    print(f"Users: {users} Total {len(users)}")
    return len(users)

def get_revenue_in_interval(start, end):
    start_date = datetime.datetime.now()
    if start!=0:
        start_date = datetime.datetime.now() - datetime.timedelta(days = start)

    end_date = datetime.datetime.now()
    if end!=0:
        end_date = datetime.datetime.now() - datetime.timedelta(days = end)
    print(Order.objects.filter(paid=True).all())

    orders = Order.objects.filter(date__gt=start_date, date__lte=end_date, paid=True)
    print(f"{start}-{end} Orders: {orders} Total {len(orders)}")

    return sum(order.total for order in orders)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def dashboard(request):
    context = dict()
    context['most_visited_product'] = get_most_visited_product_info()
    users_last_week = get_number_users_in_interval(14, 7)
    users_this_week = get_number_users_in_interval(7,0)
    msg_users =  f"{int((float(users_this_week)-float(users_last_week))*100/float(users_last_week))}% more than last week" if users_this_week>=users_last_week and users_last_week!=0 and users_this_week!=0 \
                else f"{int((float(users_last_week)-float(users_this_week))*100/float(users_this_week))}% less than last week" if users_last_week>users_this_week and users_last_week!=0 and users_this_week!=0 \
                else f"No users this week. Last week {users_last_week} new users" if users_this_week==0 \
                else f"No users last week. This week {users_this_week} new users"
    print(f"Users last week: {users_last_week}, this week: {users_this_week}")
    revenue_last_week = get_revenue_in_interval(14,7)
    revenue_this_week = get_revenue_in_interval(7,0)
    msg_revenue =  f"{int((float(revenue_this_week)-float(revenue_last_week))*100/float(revenue_last_week))}% more than last week" if revenue_this_week>=revenue_last_week and revenue_last_week!=0 and revenue_this_week!=0 \
                else f"{int((float(revenue_last_week)-float(revenue_this_week))*100/float(revenue_this_week))}% less than last week" if revenue_last_week>revenue_this_week and revenue_last_week!=0 and revenue_this_week!=0 \
                else f"No revenue this week. Last week {revenue_last_week}$ revenue" if revenue_this_week==0 \
                else f"No revenue last week. This week {revenue_this_week}$ revenue"
    print(f"Revenue last week: {revenue_last_week}, this week: {revenue_this_week}")

    context["user_info"] = msg_users
    context["revenue_info"] = msg_revenue
    return render(request, "seller/dashboard.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def stats(request):
    context = dict()
    context['products'] = Product.objects.all()
    return render(request, "seller/stats.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def manage_users(request):
    context= dict()
    context["users"] = User.objects.all()
    return render(request, "seller/users_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def manage_products(request):
    context= dict()
    context["products"] = Product.objects.all()

    return render(request, "seller/products_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def manage_orders(request):
    context= dict()
    context["orders"] = Order.objects.filter(paid=True).all()
    return render(request, "seller/orders_management.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
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
@user_passes_test(is_seller, login_url="/admin_login")
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
    context["product"] = product
    context["availability"] = Availability.objects.filter(product=product).all()
    context["specifications"] = ProductPropertiesValue.objects.filter(product=product).all()

    return render(request, "seller/edit_product.html", context=context)



@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def user_details(request):
    id = request.GET.get('id', None)

    user = User.objects.filter(id=id).first()
    context = dict()

    context["user"] = user
    context["orders"] = Order.objects.filter(user = user, paid=True).all()
    return render(request, "seller/user_details.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def admin_logout(request):
    logout(request)
    return render(request, "seller/logout.html")
@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def product_specification(request):
    id = request.GET.get('id', None)
    if request.method == "POST":
        form_data = ProductSpecificationForm(data=request.POST, files=request.FILES)
        print(form_data.errors)
        if form_data.is_valid():
            product_spec = form_data.save(commit=False)

            product_spec.save()
            return redirect("/product_details?id="+id)

    context = dict()
    context['form'] = ProductSpecificationForm(initial={"product":Product.objects.filter(id=id).first()})

    return render(request, "seller/product_specification.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def product_availability(request):
    id = request.GET.get('id', None)
    if request.method == "POST":
        form_data = AvailabilityForm(data=request.POST, files=request.FILES)
        print(form_data.errors)
        if form_data.is_valid():
            product_av = form_data.save(commit=False)

            product_av.save()
            return redirect("/product_details?id="+id)

    context = dict()
    context['form'] = AvailabilityForm(initial={"product":Product.objects.filter(id=id).first()})

    return render(request, "seller/product_availability.html", context=context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def product_specification_delete(request):
    id = request.GET.get('id', None)
    prod_spec = ProductPropertiesValue.objects.filter(id=id).first()
    prod_spec.delete()

    return redirect("/product_details/?id="+str(prod_spec.product.id))

@login_required(login_url="/admin_login")
@user_passes_test(is_seller, login_url="/admin_login")
def product_availability_delete(request):
    id = request.GET.get('id', None)
    prod_av = Availability.objects.filter(id=id).first()
    prod_av.delete()

    return redirect("/product_details/?id="+str(prod_av.product.id))


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
    context['availability'] = Availability.objects.filter(product = product).all()
    context['specifications'] = ProductPropertiesValue.objects.filter(product=product).all()
    context['show_field'] = False
    if not isinstance(request.user,AnonymousUser):
        context['shopping_cart_items'] = len(ShoppingCart.objects.filter(user__id=request.user.id).all())

        if(len(Comment.objects.filter(user=request.user, product = product).all())==0):
            context['show_field'] = True
    else:
        index = 0
        while(True):
            cookie = request.COOKIES.get('sc'+ str(index), -1)
            if cookie == -1:
                break
            index+=1


        context['shopping_cart_items'] = index
    context['form'] = CommentForm
    comments = Comment.objects.filter( product = product).all()
    context['comments'] = comments

    if request.method=="POST":
        form = CommentForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()

        return redirect("/product/?id="+id)

    product.visits = product.visits + 1
    product.save()

    return render(request, "user/product_details.html", context=context)

def register(request):
    logout(request)
    context = dict()

    if request.method == "POST":
        form = RegisterForm(data=request.POST, files=request.FILES)
        context['form'] = form
        if form.is_valid():
            user = form.save()
            login(request, user)
            group = Group.objects.filter(name='Buyer').first()
            group.user_set.add(user)
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            context['error_msg'] = "Unsuccessful registration. Invalid information."
    else:
        context['form'] = RegisterForm

    return render(request, "user/user_register.html", context)

def add_to_cart(request):

    id = request.GET.get('id', None)
    qty = request.GET.get('qty', None)
    product = Product.objects.filter(id=id).first()
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


        response.set_cookie('sc'+str(index)+"_qty", (qty if product.quantity>=int(qty) else product.quantity))
    else:
        shopping_cart_item = ShoppingCart(user = request.user,
                                            product = product,
                                            quantity=int(qty) if product.quantity>=int(qty) else product.quantity)
        shopping_cart_item.save()

    return response
def update_shopping_cart(request):

    id = request.GET.get('id', None)
    qty = request.GET.get('qty', None)
    response = HttpResponse()


    if isinstance(request.user,AnonymousUser):
        cookie_id = request.COOKIES.get('sc'+ str(id)+"_id", -1)
        product = Product.objects.filter(id=cookie_id).first()
        response.set_cookie('sc'+str(id)+"_qty", (qty if product.quantity>=int(qty) else product.quantity))
    else:

        shopping_cart_item = ShoppingCart.objects.filter(id=id).first()
        # if shopping_cart_item.product.quantity<=qty:
        #     shopping_cart_item.quantity = qty
        # else:
        #     shopping_cart_item.quantity = shopping_cart_item.product.quantity
        # product = Product.objects.filter(id=shopping_cart_item.product.id).first()
        shopping_cart_item.quantity = (int(qty) if shopping_cart_item.product.quantity>=int(qty) \
                                        else shopping_cart_item.product.quantity)
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
            order.date = datetime.datetime.now()
            order.save()
            context['order'] = order

            return render(request, "user/payment_option.html", context)
    return render(request, "user/order_info.html",context= context)

def pay_with_existing_card(request):
    context = dict()
    id = request.GET.get('id', None)
    order = Order.objects.filter(id=id).first()
    credit_card_id = request.GET.get('creditCardId', None)
    creditcard = CreditCard.objects.filter(id=credit_card_id).first()

    order_items = []
    total=0
    if isinstance(request.user,AnonymousUser):
        guest_user = User.objects.filter(username="GuestUser").first()
        # credi.user = guest_user
        order.user = guest_user

        total,order_items =add_order_items_cookie(id, request)
    else:
        total,order_items = add_order_items_db(id, request.user)
        order.user = request.user
        order.payment_option = creditcard
        shopping_cart_items = ShoppingCart.objects.filter(user=request.user).all()
        [item.delete() for item in shopping_cart_items]

    order.total = total
    order.paid = True
    order.save()
    context['order_items'] = order_items

    response = render(request, "user/payment_succesful.html", context)
    if isinstance(request.user,AnonymousUser):
        index = 0
        while(True):
            cookie_val = request.COOKIES.get('sc'+ str(index), -1)
            if cookie_val == -1:
                break
            response.delete_cookie('sc'+str(index))
            response.delete_cookie('sc'+str(index)+"_id")
            response.delete_cookie('sc'+str(index)+"_qty")
            index+=1

    return response

def add_order_items_cookie(orderId, request):
    index = 0
    total = 0
    order_items = []
    while(True):
        cookie = request.COOKIES.get('sc'+ str(index), -1)

        if cookie == -1:
            break
        order_item = OrderItem(product = Product.objects.filter(id=request.COOKIES.get('sc'+ str(index) + "_id", -1)).first(),
                               quantity = int(request.COOKIES.get('sc'+ str(index)+"_qty", -1)),
                               order = Order.objects.filter(id=orderId).first())

        total += order_item.product.price * order_item.quantity
        product = Product.objects.filter(id=order_item.product.id).first()
        product.quantity = product.quantity- order_item.quantity
        order_item.save()
        product.save()
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

        product = Product.objects.filter(id=order_item.product.id).first()
        product.quantity = product.quantity- order_item.quantity
        order_item.save()
        product.save()
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
            if creditcard.expires_on <datetime.date.today() or len(creditcard.number)!=16 \
                or len(creditcard.ccv)!=4 or not creditcard.number.isnumeric() or not creditcard.ccv.isnumeric():

                if creditcard.expires_on <datetime.date.today():
                    context['error_msg'] = 'Expired card'
                elif len(creditcard.number)!=16 or not creditcard.number.isnumeric():
                    context['error_msg'] = 'Invalid credit card number'
                elif len(creditcard.ccv)!=4 or not creditcard.ccv.isnumeric():
                    context['error_msg'] = 'Invalid credit card CCV'
                context['form'] = PaymentForm
                return render(request, "user/payment_form.html", context)
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
                shopping_cart_items = ShoppingCart.objects.filter(user=request.user).all()
                [item.delete() for item in shopping_cart_items]
                creditcard.save()
                order.payment_option = creditcard
            order.total = total
            order.date = datetime.datetime.now()
            order.paid = True
            order.save()
            context['order_items'] = order_items
            response = render(request, "user/payment_succesful.html", context)
            if isinstance(request.user,AnonymousUser):
                index = 0
                while(True):
                    cookie_val = request.COOKIES.get('sc'+ str(index), -1)
                    if cookie_val == -1:
                        break
                    response.delete_cookie('sc'+str(index))
                    response.delete_cookie('sc'+str(index)+"_id")
                    response.delete_cookie('sc'+str(index)+"_qty")
                    index+=1

            return response
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

def locator(request):
    context = dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
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
    return render(request, "user/locator.html", context)

def search_products(request):
    context = dict()
    context['brands'] = Brand.objects.all()
    context['categories']= Category.objects.all()
    q = request.GET.get('q', None)
    products = Product.objects.filter(Q(name__contains=q) | Q(description__contains=q)).all()
    context['products'] = products
    context['title'] = f"Results for query {q}"
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

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def search_products_admin(request):
    context = dict()
    q = request.GET.get('q', None)
    products = Product.objects.filter(Q(name__contains=q) | Q(description__contains=q)).all()
    context['products'] = products
    return render(request, "seller/search_results_products.html", context)

@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def search_orders(request):
    context = dict()
    q = request.GET.get('q', None)
    orders = Order.objects.filter((Q(name__contains=q) | Q(user__username__contains=q) |
                                  Q(surname__contains=q) | Q(address__contains=q) |
                                  Q(city__contains=q)) & Q(paid=True)).all()
    context['orders'] = orders
    return render(request, "seller/search_results_orders.html", context)



@login_required(login_url="/admin_login")
@user_passes_test(is_seller)
def search_users(request):
    context = dict()
    q = request.GET.get('q', None)
    users = User.objects.filter(Q(username__contains=q)).all()
    context['users'] = users
    return render(request, "seller/search_results_users.html", context)

