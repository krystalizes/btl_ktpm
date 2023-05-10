from datetime import timezone

from django.http import JsonResponse
from datetime import datetime
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import order
import requests
import json
from .serializers import OrderSerializer


class GetOrderAPIView(APIView):
    def get(self, request, id):
        try:
            order_obj = order.objects.get(id=id)
            serializer = OrderSerializer(order_obj, partial=True)
            response_data = {
                'status': 'Success',
                'message': [serializer.data]
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except order.DoesNotExist:
            return JsonResponse({'message': 'Order does not exist'}, status=401)
class GetOrderlistCustomerAPIView(APIView):
    def get(self,request,uid):
        try:
            order_obj = order.objects.filter(customerid=uid)
            serializer = OrderSerializer(order_obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except order.DoesNotExist:
            return JsonResponse({'message': 'Customer does not exist'}, status=401)
class RegisOrderAPIView(APIView):
    def post(self, request):
        customerid=request.data.get('customerid')
        if customerid:
            url_cart = 'http://127.0.0.1:8005/get_cart/' + customerid + "/"
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url_cart, headers=headers)
            val1 = json.loads(response.content.decode('utf-8'))
            status1 = val1['status']
            data = val1['message']
            total_price = 0
            total_quantity=0
            productlist=''
            status2="Processing"
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if status1 == "Success":
                for item in data:
                    price = int(item['price'])
                    quantity=int(item['quantity'])
                    productlist+=item['product_id']+'x'+str(quantity)+' '
                    total_price += price
                    total_quantity += quantity
                url_cart_delete = 'http://127.0.0.1:8005/cart_delete_all/' + customerid + "/"
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url_cart_delete, headers=headers)
                val2 = json.loads(response.content.decode('utf-8'))
                data = {
                    'customerid': customerid,
                    'productlist': productlist,
                    'quantity': total_quantity,
                    'price': total_price,
                    'status': status2,
                    'created_at': created_at
                }
                serializer = OrderSerializer(data=data)

                # Validate the data and save it to the database
                if serializer.is_valid():
                    serializer.save()
                    serialized_data = serializer.data
                    serialized_data['status'] = 'Success'
                    serialized_data = [serialized_data]  # convert to list for consistent format
                    response_data = {
                        "status": "Success",
                        "message": serialized_data
                    }
                    url_shipment = 'http://127.0.0.1:8002/shipment_regis/'
                    headers = {'Content-Type': 'application/json'}
                    data2 = {'orderid': serializer.instance.id, 'shipping_method': 'Not choosed'}
                    response = requests.post(url_shipment, data=json.dumps(data2), headers=headers)
                    url_payment = 'http://127.0.0.1:8003/payment_regis/'
                    headers = {'Content-Type': 'application/json'}
                    data3 = {'orderid': serializer.instance.id, 'payment_method': 'Not choosed', 'price': serializer.instance.price}
                    response = requests.post(url_payment, data=json.dumps(data3), headers=headers)
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "status": "Error",
                        "message": serializer.errors
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {
                    "status": "Error",
                    "message": "Failed to retrieve cart items."
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = {
                "status": "Error",
                "message": "Missing customer ID."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



