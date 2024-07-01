from django.urls import path

from mini_pos_django import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [

    path('', views.index, name='home'),

    #Auth
    path('signin', views.signIn, name='sign'),
    path('signup', views.singUp, name='signup'),
    path('logout/<int:user_id>', views.logout, name='logout'),

    # Customer
    path('customer', views.getCustomer, name='customer'),
    path('customer/<int:customer_id>/', views.getCustomerByID, name='customer_detail'),
    path('customer/<int:customer_id>/delete', views.delete_customer, name='delete_customer'),
    path('customer/<int:customer_id>/update', views.update_customer, name='update_customer'),
    path('customer/create', views.save_customer, name='save_customer'),
    

    #Product
    path('product', views.getProduct, name='product'),
    path('product/<int:product_id>/', views.getProductByID, name='product_detail'),
    path('product/<int:product_id>/delete', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/update', views.update_product, name='update_product'),
    path('product/create', views.save_product, name='save_product'),


    #Order
    path('order', views.getOrder, name='order'),
    path('order/create', views.save_order, name='save_order'),

]+ static(settings.MEDIA_URL, # type: ignore
                              document_root=settings.MEDIA_ROOT)

# urlpatterns = [

#     path('', views.index, name="home"),

#     # Customer
#     path('customer', views.customer, name='customer'),
#     path('customer/<int:customer_id>', views.delete_customer, name='delete_customer'),
#     path('customer/update/<int:customer_id>', views.update_customer, name='update_customer'),
    

#     #Product
#     path('product', views.getProduct, name='product'),
#     path('product/<int:product_id>', views.delete_product, name='delete_product'),
#     path('product/<int:product_id>', views.update_product, name='update_product'),


#     #Order
#     path('order', views.order, name='order'),

# ]