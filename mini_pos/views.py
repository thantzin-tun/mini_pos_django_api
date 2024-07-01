# import json
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import redirect, render

# from mini_pos.forms import CustomerForm, OrderForm, ProductForm
# from mini_pos.models import Customer, Order, Product
# # 1. request -> response
# # 2. request -> handler
# # 3. action

# def index(request):
#     return render(request, 'home.html')

# #For Customer
# def customer(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customer')
#     elif request.method == "GET":
#         customers = Customer.objects.all()
#         form = CustomerForm()
#         context = {
#             "customers" : customers,
#             'form' : form
#         }    
#         return render(request,'customer.html',context)


# def delete_customer(request,customer_id):
#     if request.method == "DELETE":
#         try:
#             customer = Customer.objects.get(id=customer_id)
#             customer.delete()
#             return JsonResponse({'status': 'success', 'message': 'Customer deleted successfully'})
#         except Product.DoesNotExist:
#             return JsonResponse({'status': 'failed', 'error': 'Customer not found'}, status=404)


# def update_customer(request,customer_id):
  
#         customer = Customer.objects.get(id=customer_id)
#         context = {
#             'form' : CustomerForm(customer)
#         }
#         return render(request,'customer_form.html',context)


# #For Product
# def getProduct(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('product')
#     elif request.method == "GET":
#         products = Product.objects.all()
#         form = ProductForm()
#         context = {
#             "products" : products,
#             'form' : form
#         }    
#         return render(request,'product.html',context)

# def delete_product(request,product_id):
#         if request.method == 'DELETE':
#             try:
#                 product = Product.objects.get(id=product_id)
#                 product.delete()
#                 return JsonResponse({'status': 'success', 'message': 'Product deleted successfully'})
#             except Product.DoesNotExist:
#                 return JsonResponse({'status': 'failed', 'error': 'Product not found'}, status=404)

# def update_product(request,product_id):
#     if request.method == 'PUT':
#         return JsonResponse({'status': 'failed', 'error': 'Product not found'}, status=404)    



# def order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order')
#     elif request.method == "GET":
#         orders = Order.objects.all()
#         form = OrderForm()
#         context = {
#             "orders" : orders,
#             'form' : form
#         }    
#         return render(request,'order.html',context)



    # @api_view(['POST'])
    # def save_customer(request):
    #     data = request.POST
    #     resp = {'status' : "failed"}
    #     if data:
    #         customer = Customer()
    #         customer.name = data['name']
    #         customer.phone = data['phone']
    #         customer.address = data['address']
    #         if data['isCustomer'] == 'true':
    #             customer.isCustomer = True
    #         else:
    #             customer.isCustomer = False
    #         customer.save()
    #         resp['status'] = 'success'
    #         resp['customer'] = customer
    #         return HttpResponse(json.dumps(resp), content_type="application/json")




from django.shortcuts import get_object_or_404, render

from mini_pos.models import Customer, Order, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mini_pos.serializer import CustomerSerializer, OrderSerializer, ProductSerializer


from django.core.exceptions import ObjectDoesNotExist
# 1. request -> response
# 2. request -> handler
# 3. action

from rest_framework.response import Response # type: ignore
from .serializer import UserSerializer
from rest_framework import status # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,authentication_classes,permission_classes # type: ignore
from rest_framework.authentication import SessionAuthentication,TokenAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated# type: ignore


@api_view(["POST"])
def singUp(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token" : token.key,"user" : {"id" : serializer.data['id'],"username" : serializer.data['username']},"status": status.HTTP_200_OK,"message" : "success"})
    else:
        return Response({"message": serializer.errors['username'][0],"status" :status.HTTP_400_BAD_REQUEST,"token" :"", "user": None})


@api_view(["POST"])
def signIn(request):
    print(request.data['username'])
    print(request.data['password'])
    try:
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            token, created = Token.objects.get_or_create(user=user) 
            serializer = UserSerializer(instance=user)
            return Response({"token" : token.key,"user" : {"id" : serializer.data['id'],"username" : serializer.data['username']},"message": "အောင်မြင်ပါသည်"})
        else:
           return Response({"token" : "","user" : None,"message": "pass"},status= status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"user" : None,"message": "user","token":""},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def logout(request,user_id):
    hasToken = Token.objects.get(user_id= user_id)
    if hasToken:
        hasToken.delete()
        return Response({"status": status.HTTP_200_OK})
    else:
        return Response({"status": status.HTTP_400_BAD_REQUEST,"user" : "No user found!"})



def index(request):
    products = Customer.objects.all()
    return render(request, 'home.html',{'products':products})


# For Customer
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def getCustomer(request):
    customers = Customer.objects.all()
    paginate = Paginator(customers, 10) 
    page_number = request.query_params.get('page', 1)
    try:
        page_obj = paginate.page(page_number)
    except PageNotAnInteger:
        page_obj = paginate.page(1)
    except EmptyPage:
        page_obj = paginate.page(paginate.num_pages)

    serializer = CustomerSerializer(page_obj, many=True)
    return Response({"customers" : serializer.data,
                     "count": paginate.count,
                     "pages" : paginate.num_pages,
                     "next_page": page_obj.next_page_number() if  page_obj.has_next() else None,
                     "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None })

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def getCustomerByID(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"customer": ""}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def save_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'customer': serializer.data})
    else:
        return Response({'status': 'failed', 'errors': serializer.errors}, status=400)
    
#Delete
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response({'status': 'success', 'message': 'Customer deleted successfully'})
    except Customer.DoesNotExist:
        return Response({'status': 'failed', 'error': 'Customer not found'}, status=404)


@api_view(['PATCH', 'PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def update_customer(request,customer_id):
    if request.method == 'PATCH':    
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer, data=request.data,partial=True)
            return check_validate(serializer)
        except Customer.DoesNotExist:
            return Response({'status': 'failed', 'error': 'Customer not found'}, status=404)
    else:
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer, data=request.data)
            return check_validate(serializer)
        except Customer.DoesNotExist:
            return Response({'status': 'failed', 'error': 'Customer not found'}, status=404)


def check_validate(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'customer': serializer.data}, status=200)
    else:
        return Response({'status': 'failed', 'errors': serializer.errors}, status=404)



#For Product
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def getProduct(request):
    products = Product.objects.all()
    paginate = Paginator(products, 10) 
    page_number = request.query_params.get('page', 1)
    try:
        page_obj = paginate.page(page_number)
    except PageNotAnInteger:
        page_obj = paginate.page(1)
    except EmptyPage:
        page_obj = paginate.page(paginate.num_pages)

    serializer = ProductSerializer(page_obj, many=True)
    return Response({"products" : serializer.data,
                     "count": paginate.count,
                     "pages" : paginate.num_pages,
                     "next_page": page_obj.next_page_number() if  page_obj.has_next() else None,
                     "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None })

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def getProductByID(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"product": ""}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def save_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'product': serializer.data})
    else:
        return Response({'status': 'failed', 'errors': serializer.errors}, status=400)
    

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response({'status': 'success', 'message': 'Product deleted successfully'},status=200)
    except Product.DoesNotExist:
        return Response({'status': 'failed', 'error': 'Product not found'}, status=404)


@api_view(['PATCH', 'PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def update_product(request,product_id):
    if request.method == 'PATCH':    
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data,partial=True)
            return check_validate(serializer)
        except Product.DoesNotExist:
            return Response({'status': 'failed', 'error': 'Product not found'}, status=404)
    else:
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data)
            return check_validate(serializer)
        except Product.DoesNotExist:
            return Response({'status': 'failed', 'error': 'Product not found'}, status=404)


def check_validate(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'product': serializer.data}, status=200)
    else:
        return Response({'status': 'failed', 'errors': serializer.errors}, status=404)






#Order
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def getOrder(request):
    customer_id = request.query_params.get('customer_id')
    product_id = request.query_params.get('product_id')
    total = request.query_params.get('total')
    is_paid = request.query_params.get('is_paid')

    orders = Order.objects.all()
    if customer_id:
        orders = orders.filter(customer_id=customer_id)
    if product_id:
        orders = orders.filter(product_id=product_id)
    if total:
        orders = orders.filter(total=total)
    if is_paid:
        orders = orders.filter(is_paid=is_paid)

    paginate = Paginator(orders, 5)
    page_number = request.query_params.get('page', 1)
    try:
        page_obj = paginate.page(page_number)
    except PageNotAnInteger:
        page_obj = paginate.page(1)
    except EmptyPage:
        page_obj = paginate.page(paginate.num_pages)

    serializer = OrderSerializer(page_obj, many=True)
    return Response({
        "orders": serializer.data,
        "count": paginate.count,
        "pages": paginate.num_pages,
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None
    })


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])  
def save_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'customer': serializer.data})
    else:
        return Response({'status': 'failed', 'errors': serializer.errors}, status=400)

















    # @api_view(['POST'])
    # def save_customer(request):
    #     data = request.POST
    #     resp = {'status' : "failed"}
    #     if data:
    #         customer = Customer()
    #         customer.name = data['name']
    #         customer.phone = data['phone']
    #         customer.address = data['address']
    #         if data['isCustomer'] == 'true':
    #             customer.isCustomer = True
    #         else:
    #             customer.isCustomer = False
    #         customer.save()
    #         resp['status'] = 'success'
    #         resp['customer'] = customer
    #         return HttpResponse(json.dumps(resp), content_type="application/json")





















