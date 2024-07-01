from django import forms
from django.forms import ModelForm
from .models import Customer, Order, Product

# Create the form class.

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','phone','address','email','isCustomer']
        



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price_per_unit','unit','description','stock']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','product','quantity','total','is_paid','notes']