from django import forms
from shop.models import Product

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