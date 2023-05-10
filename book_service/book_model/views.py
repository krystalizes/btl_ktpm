from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import books
@csrf_exempt
def get_all_book(request):
    data = []
    resp = {}
# This will fetch the data from the database.
    prodata = books.objects.all()
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
def data_insert(id, name, author, availability, description, price):
    books_data = books(id = id, name = name, author = author, availability = availability,description=description, price = price)
    books_data.save()
    return 1
def check_book_exists(id):
    try:
        book = books.objects.get(id=id)
        return True
    except books.DoesNotExist:
        return False
### This function will get the data from the front end.
@csrf_exempt
def book_regis(request):
    ### The Following are the input fields.
    id = request.POST.get("Book Id")
    name = request.POST.get("Name")
    author = request.POST.get("Author")
    availability = request.POST.get("Availability")
    description = request.POST.get("Description")
    price = request.POST.get("Price")
    resp = {}
    if id and name and author and availability and description and price:
    #### In this if statement, checking that all fields are available.
        a = check_book_exists(id)
        if not a:
            respdata = data_insert(id, name, author, availability, description, price)
            ### If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Book is registered Successfully.'
            ### If it is not returning any value then the show willfail.
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Unable to register Book, Please try again.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Book already exist, Please use another ID.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')
def book_data(uname):
    book = books.objects.filter(id = uname)
    for data in book.values():
        return data
@csrf_exempt
def book_info(request, pid):
    resp = {}
    if pid:
## Calling the getting the user info.
        respdata = book_data(pid)
        dict1 = {}
        if respdata:
            dict1['Book Id'] = respdata.get('id','')
            dict1['Name'] = respdata.get('name','')
            dict1['Author'] = respdata.get('author','')
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
def update_book(request, id):
    resp = {}
    try:
        book = books.objects.get(id=id)
    except books.DoesNotExist:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Book does not exist.'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    if request.method == 'PATCH':
        data = json.loads(request.body.decode('utf-8'))
        # Update the book instance with the data
        for key, value in data.items():
            setattr(book, key, value)
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = 'Book is updated Successfully.'

    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        # Update the book instance with the data
        book.name = data['name']
        book.author = data['author']
        book.availability = data['availability']
        book.description = data['description']
        book.price = data['price']
        resp['status'] = 'Success'
        resp['status_code'] = '200'
        resp['message'] = 'Book is updated Successfully.'
    book.save()

    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def data_delete(id):
    try:
        book = books.objects.get(id=id)
    except books.DoesNotExist:
        return 0

    book.delete()
    return 1

@csrf_exempt
def book_delete(request, id):
    resp = {}

    if id:
        respdata = data_delete(id)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Book is deleted Successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Unable to delete Book, Please try again.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Book ID is mandatory.'

    return HttpResponse(json.dumps(resp), content_type = 'application/json')