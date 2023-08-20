from django import forms
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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