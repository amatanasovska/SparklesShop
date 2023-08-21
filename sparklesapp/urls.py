"""
URL configuration for sparklesapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('add_specification', product_specification, name="add_specification_product"),
    path('add_availability', product_availability, name="add_availability_product"),
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('login/', user_login, name="login"),
    path('admin_login/', admin_login, name="admin_login"),
    path('register/', register,name="register"),
    # actual login
    path('user_login/', page_login, name="user_login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('users/', manage_users, name="manage_users"),
    path('products/', manage_products, name="manage_products"),
    path('orders/', manage_orders, name="manage_orders"),
    path('add_product/', add_product, name="manage_orders"),
    path('product_details/', product_details, name="product_details"),
    path('user_details/', user_details, name="user_details"),
    path('admin_logout/', admin_logout, name="admin_logout"),
    path('categories/', categories, name="categories"),
    path('brands/', brands, name="brands"),
    path('product/', product, name="product"),
    path('signout/', signout, name="signout"),
    path('add_to_cart', add_to_cart, name="add_to_cart"),
    path('update_shopping_cart', update_shopping_cart, name ="update_shopping_cart"),
    path('shopping_cart', shopping_cart, name="shopping_cart"),
    path('delete_sc_product', delete_sc_product, name="delete_sc_product"),
    path('checkout', checkout, name="checkout"),
    path("payment_info", payment_info, name = "payment_info"),
    path("order_details", order_details, name = "order_details"),
    path("locator", locator, name = "locator"),
    path("delete_spec", product_specification_delete, name="delete_spec"),
    path("delete_availability", product_availability_delete, name="delete_availability"),
    path("search", search_products, name="search" )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
