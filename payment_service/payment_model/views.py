from datetime import timezone, timedelta

from django.http import JsonResponse
from datetime import datetime
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import payment
import requests
import json
from .serializers import PaymentSerializer


class GetPaymentAPIView(APIView):
    def get(self, request, oid):
        try:
            payment_obj = payment.objects.get(orderid=oid)
            serializer = PaymentSerializer(payment_obj,partial=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except payment.DoesNotExist:
            return JsonResponse({'message': 'Payment does not exist'}, status=401)
class RegisPaymentAPIView(APIView):
    def post(self, request):
        orderid=request.data.get('orderid')
        payment_method=request.data.get('payment_method')
        price=request.data.get('price')
        if orderid:
            url_order = 'http://127.0.0.1:8008/getorderinfo/' + str(orderid) + "/"
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url_order, headers=headers)
            val1 = json.loads(response.content.decode('utf-8'))
            status1 = val1['status']
            now = datetime.now()
            payment_done_date=now.strftime('%Y-%m-%d %H:%M:%S')
            status2="Not paid"
            if status1 == "Success":
                data = {
                    'orderid': orderid,
                    'status': status2,
                    'payment_method': payment_method,
                    'price': price,
                    'payment_done_date': payment_done_date
                }
                serializer = PaymentSerializer(data=data)

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

