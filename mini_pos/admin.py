from django.contrib import admin

admin.site.site_header = "Mini POS"
admin.site.site_title = "Mini POS"
admin.site.index_title = "Mini POS"


# Register your models here.
from .models import Customer,Order,Product
admin.site.register(Customer)
admin.site.register(Order)
