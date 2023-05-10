from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import carts


### This function is inserting the data into our table.
def cart_data_insert(customerid, product_id, quantity, price):
    cart_data = carts(customerid=customerid, product_id=product_id, quantity=quantity, price=price)
    cart_data.save()
    return 1


### This function will get the data from the front end.
@csrf_exempt
def cart_regis(request):
    # val1 = json.loads(request.body)
    ### This is for reading the inputs from JSON.
    customerid = request.POST.get("Customer Id")
    product_id = request.POST.get("Product Id")
    quantity = request.POST.get("Quantity")
    resp = {}
    url = 'http://127.0.0.1:8000/getcustomerinfo/'+customerid+"/"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    val1 = json.loads(response.content.decode('utf-8'))
    if val1 == "Customer exist":
        url_book = 'http://127.0.0.1:8004/book_info/'+product_id+"/"
        url_clothe = 'http://127.0.0.1:8006/clothe_info/'+product_id+"/"
        url_shoe = 'http://127.0.0.1:8007/shoe_info/'+product_id+"/"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url_book, headers=headers)
        val1 = json.loads(response.content.decode('utf-8'))
        response = requests.get(url_clothe,  headers=headers)
        val2 = json.loads(response.content.decode('utf-8'))
        response = requests.get(url_shoe,  headers=headers)
        val3 = json.loads(response.content.decode('utf-8'))
        status1 = val1['status']
        status2 = val2['status']
        status3 = val3['status']
        if status1=="Success" :
            ### After all validation, it will call the data_insertfunction.
            price1= int(val1['data']['Price'])*int(quantity)
            respdata = cart_data_insert(customerid, product_id, quantity, price1)
            ### If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Cart is added Successfully.'
        elif status2=="Success" :
            price2= int(val2['data']['Price'])*int(quantity)
            ### After all validation, it will call the data_insertfunction.
            respdata = cart_data_insert(customerid, product_id, quantity, price2)
            ### If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Cart is added Successfully.'
        elif status3=="Success" :
            price3= int(val3['price'])*int(quantity)
            ### After all validation, it will call the data_insertfunction.
            respdata = cart_data_insert(customerid, product_id, quantity, price3)
            ### If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Cart is added Successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Product does not exist.'
    ### If value is not found then it will give failed in response.
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'User does not exist.'
    return HttpResponse(json.dumps(resp), content_type='application/json')
### This function is used for getting the shipment status
@csrf_exempt
def get_cart_data(request,uid):
    respdata = []
    resp = {}
    data = carts.objects.filter(customerid=uid)
    for val in data.values():
        respdata.append(val)
    ### It will call the shipment_data function.

    ### If it returns value then will show success.
    if respdata:
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = respdata
        ### If it is not returning any value then it will show failed response.
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Cart data is not available.'
    return HttpResponse(json.dumps(resp), content_type='application/json')
def data_update(uid, pid, quantity, price):
    try:
        cart = carts.objects.get(customerid=uid,product_id=pid)
    except carts.DoesNotExist:
        return 0

    if quantity is not None:
        cart.quantity = quantity
        cart.price = price

    cart.save()
    return 1

@csrf_exempt
def update_cart(request, uid, pid):
    resp = {}
    try:
        cart = carts.objects.get(customerid=uid,product_id=pid)
        old_quantity=int(cart.quantity)
        old_price=cart.price
    except carts.DoesNotExist:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Cart product does not exist.'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    if request.method == 'PATCH':
        data = json.loads(request.body.decode('utf-8'))
        # Update the cart instance with the data
        a=data.get("quantity")
        quantity = int(a)
        price = old_price/old_quantity*quantity
        respdata=data_update(uid, pid, a, price)
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = 'Cart product is updated Successfully.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def product_delete(uid,pid):
    try:
        cart = carts.objects.get(customerid=uid,product_id=pid)
    except carts.DoesNotExist:
        return 0

    cart.delete()
    return 1

@csrf_exempt
def cart_delete_product(request, uid, pid):
    resp = {}

    if uid and pid:
        respdata = product_delete(uid, pid)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Cart Product is deleted Successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Unable to delete Product from Cart, Please try again.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Customer ID or Product ID is missing.'

    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def product_delete_all(uid):

    try:
        cart = carts.objects.filter(customerid=uid)
        for val in cart.values():
            cart.delete()
    except carts.DoesNotExist:
        return 0
    return 1

@csrf_exempt
def cart_delete(request,uid):
    resp = {}

    if uid:
        respdata = product_delete_all(uid)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Cart is deleted Successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Unable to delete Cart, Please try again.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Customer ID is missing.'

    return HttpResponse(json.dumps(resp), content_type = 'application/json')