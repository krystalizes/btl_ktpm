from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import clothes
@csrf_exempt
def get_all_clothe(request):
    data = []
    resp = {}
# This will fetch the data from the database.
    prodata = clothes.objects.all()
    for tbl_value in prodata.values():
        data.append(tbl_value)
# If data is available then it returns the data.
    if data:
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['data'] = data
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Data is not available.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def data_insert(id, name, brand, availability, description, price):
    clothe_data = clothes(id = id, name = name, brand = brand, availability = availability,description=description, price = price)
    clothe_data.save()
    return 1
def check_clothe_exists(id):
    try:
        clothe = clothes.objects.get(id=id)
        return True
    except clothes.DoesNotExist:
        return False
### This function will get the data from the front end.
@csrf_exempt
def clothe_regis(request):
    ### The Following are the input fields.
    id = request.POST.get("Clothe Id")
    name = request.POST.get("Name")
    brand = request.POST.get("Brand")
    availability = request.POST.get("Availability")
    description = request.POST.get("Description")
    price = request.POST.get("Price")
    resp = {}
    if id and name and brand and availability and description and price:
    #### In this if statement, checking that all fields are available.
        a = check_clothe_exists(id)
        if not a:
            respdata = data_insert(id, name, brand, availability, description, price)
            ### If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Clothe is registered Successfully.'
            ### If it is not returning any value then the show willfail.
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Unable to register Clothe, Please try again.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Clothe already exist, Please use another ID.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def clothe_data(uname):
    clothe = clothes.objects.filter(id = uname)
    for data in clothe.values():
        return data
@csrf_exempt
def clothe_info(request,pid):
    resp = {}
    if pid:
## Calling the getting the user info.
        respdata = clothe_data(pid)
        dict1 = {}
        if respdata:
            dict1['Clothe Id'] = respdata.get('id','')
            dict1['Name'] = respdata.get('name','')
            dict1['Brand'] = respdata.get('brand','')
            dict1['Availability'] = respdata.get('availability','')
            dict1['Description'] = respdata.get('description','')
            dict1['Price'] = respdata.get('price', '')
        if dict1:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['data'] = dict1
### If a user is not found then it give failed as a response.
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['data'] = 'Product Not Found.'
        ### The field value is missing.
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['data'] = 'Fields is mandatory.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')
@csrf_exempt
def update_clothe(request, pid):
    resp = {}
    try:
        clothe = clothes.objects.get(id=pid)
    except clothes.DoesNotExist:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Clothe does not exist.'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    if request.method == 'PATCH':
        data = json.loads(request.body.decode('utf-8'))
        # Update the clothe instance with the data
        for key, value in data.items():
            setattr(clothe, key, value)
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = 'Clothe is updated Successfully.'

    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        # Update the book instance with the data
        clothe.name = data['name']
        clothe.brand = data['brand']
        clothe.availability = data['availability']
        clothe.description = data['description']
        clothe.price = data['price']
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = 'Clothe is updated Successfully.'
    clothe.save()

    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def data_delete(pid):
    try:
        clothe = clothes.objects.get(id=pid)
    except clothes.DoesNotExist:
        return 0
    clothe.delete()
    return 1

@csrf_exempt
def clothe_delete(request,pid):
    resp = {}

    if pid:
        respdata = data_delete(pid)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Clothe is deleted Successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Unable to delete Clothe, Please try again.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Clothe ID is mandatory.'

    return HttpResponse(json.dumps(resp), content_type = 'application/json')