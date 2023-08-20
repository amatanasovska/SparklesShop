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
    
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

class Order(models.Model):
    pass

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Store(models.Model):
    location = models.CharField(max_length=20, choices=(('SK', 'Skopje'),
                                                        ('BT', 'Bitola'),
                                                        ('PR', 'Prilep'),
                                                        ('VE', 'Veles'),
                                                        ('SR', 'Strumica')))

class Availability(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

class ProductProperty(models.Model):
    name = models.CharField(max_length=50)

class ProductPropertiesValue(models.Model):
   product_property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   value = models.CharField(max_length=255)





