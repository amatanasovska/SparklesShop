from django import forms
from shop.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductSpecificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductSpecificationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = ProductPropertiesValue
        fields = "__all__"
class AvailabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Availability
        fields = "__all__"
          
class ProductForm(forms.ModelForm):
    # fields = ("name", "quantity", "price",
    #                "image", "description", "category")
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Product
        
        fields = ("name", "quantity", "price",
                   "image", "description", "category", "brand")
        
# class RegisterForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         for field in self.visible_fields():
#             field.field.widget.attrs["class"] = "form-control"
#     class Meta:
#         model = User
#         fields = ["username", "password", "first_name", "last_name", "email"]

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class OrderForm(forms.ModelForm):
    # fields = ("name", "quantity", "price",
    #                "image", "description", "category")
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Order
        exclude = ("user","payment_option","total","paid")
        

class PaymentForm(forms.ModelForm):
    # fields = ("name", "quantity", "price",
    #                "image", "description", "category")
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = CreditCard
        widgets= {
        'expires_on': forms.DateInput(attrs={'type': 'date'}) 
        }
        exclude = ("user",)
        

class CommentForm(forms.ModelForm):
    # fields = ("name", "quantity", "price",
    #                "image", "description", "category")
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Comment
        exclude = ("product","user")
        