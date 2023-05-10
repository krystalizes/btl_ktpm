from datetime import timezone, timedelta

from django.http import JsonResponse
from datetime import datetime
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import shipment
import requests
import json
from .serializers import ShipmentSerializer


class GetShipmentAPIView(APIView):
    def get(self, request, oid):
        try:
            shipment_obj = shipment.objects.get(orderid=oid)
            serializer = ShipmentSerializer(shipment_obj,partial=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except shipment.DoesNotExist:
            return JsonResponse({'message': 'Shipment does not exist'}, status=401)
class RegisShipmentAPIView(APIView):
    def post(self, request):
        orderid=request.data.get('orderid')
        shipping_method=request.data.get('shipping_method')
        if orderid:
            url_order = 'http://127.0.0.1:8008/getorderinfo/' + str(orderid) + "/"
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url_order, headers=headers)
            val1 = json.loads(response.content.decode('utf-8'))
            status1 = val1['status']
            customerid = val1['message'][0]['customerid']
            now = datetime.now()
            estimated = now + timedelta(days=7)
            estimated_date = estimated.strftime('%Y-%m-%d')
            actual_date=now.strftime('%Y-%m-%d')
            status2="Shipping"
            if status1 == "Success":
                url_customer = 'http://127.0.0.1:8000/getcustomerinfo2/' + str(customerid) + "/"
                headers = {'Content-Type': 'application/json'}
                response = requests.get(url_customer, headers=headers)
                val2 = json.loads(response.content.decode('utf-8'))
                mobile = val2['phone']
                shipping_address = val2['address']
                data = {
                    'orderid': orderid,
                    'status': status2,
                    'mobile': mobile,
                    'shipping_address': shipping_address,
                    'shipping_method': shipping_method,
                    'estimated_delivery_date': estimated_date,
                    'actual_delivery_date':actual_date
                }
                serializer = ShipmentSerializer(data=data)

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
                    "message": "Failed to retrieve order info."
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = {
                "status": "Error",
                "message": "Missing Order ID."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

