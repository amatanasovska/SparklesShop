from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images', blank=True)
    description = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.name
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    number = models.CharField(max_length=16)
    ccv = models.CharField(max_length=4)
    expires_on = models.DateField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    email = models.EmailField()
    payment_option = models.ForeignKey(CreditCard, on_delete=models.CASCADE, blank=True, null=True)
    total = models.IntegerField()
    paid = models.BooleanField()

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Store(models.Model):
    location = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.location

class Availability(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

class ProductProperty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class ProductPropertiesValue(models.Model):
   product_property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   value = models.CharField(max_length=255)





