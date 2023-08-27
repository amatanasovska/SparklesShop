from django.contrib import admin

from shop.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    exclude = ('visits', )


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Brand, BrandAdmin)

class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('user','product','quantity')


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(ShoppingCart, ShoppingCartAdmin)



class ProductPropertyAdmin(admin.ModelAdmin):
    fields = ('name',)


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(ProductProperty, ProductPropertyAdmin)

class ProductPropertiesValueAdmin(admin.ModelAdmin):
    fields = ('product_property', 'product', 'value')


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(ProductPropertiesValue, ProductPropertiesValueAdmin)

class StoreAdmin(admin.ModelAdmin):
    fields = ('location',)


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Store, StoreAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    fields = ("user", "full_name", "expires_on")


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(CreditCard, CreditCardAdmin)

class OrderAdmin(admin.ModelAdmin):
    fields = ("user", "name", "surname", "address", "city",
              "postal_code","email","payment_option","total",
              "date","paid")


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    fields = ("product", "quantity", "order")


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(OrderItem, OrderItemAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields = ("user", "product", "content")


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Comment, CommentAdmin)

class AvailabilityAdmin(admin.ModelAdmin):
    fields = ("store", "product")
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
admin.site.register(Availability, AvailabilityAdmin)