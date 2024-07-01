from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=0) 
    unit = models.CharField(max_length=255)
    description = models.CharField(max_length=255,null=True,blank=True)
    stock = models.DecimalField(max_digits=6,decimal_places=0)
    product_image = models.ImageField(blank=True,null=True,upload_to='product/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='customer/',null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    isCustomer = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name 

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=8, decimal_places=2) 
    notes = models.CharField(max_length=255,null=True)
    is_paid = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
   