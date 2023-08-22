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
    fields = ('name',)


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
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(CreditCard, CreditCardAdmin)

class OrderAdmin(admin.ModelAdmin):
    fields = ("user", )


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Order, OrderAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields = ("user", )


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(Comment, CommentAdmin)