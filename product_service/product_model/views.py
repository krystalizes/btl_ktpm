# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import product_details
@csrf_exempt
def get_product_data(request):
    url_book= 'http://127.0.0.1:8004/getallbook/'
    url_clothe = 'http://127.0.0.1:8006/getallclothe/'
    url_shoe = 'http://127.0.0.1:8007/getallshoe/'
    data = {}
    data['status'] = 'Success'
    data['status_code'] = '200'
    data['message'] = "All Product"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url_book, headers=headers)
    val1 = json.loads(response.content.decode('utf-8'))
    response = requests.get(url_clothe, headers=headers)
    val2 = json.loads(response.content.decode('utf-8'))
    response = requests.get(url_shoe, headers=headers)
    val3 = json.loads(response.content.decode('utf-8'))
    data["data"]={
        "book":val1['data'],
        "clothe":val2['data'],
        "shoe": val3,
    }
    return HttpResponse(json.dumps(data), content_type = 'application/json')

