from django.http import JsonResponse


# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user,customer
import requests
import json


from .serializers import UserSerializer, CustomerSerializer


class LoginAPIView(APIView):
    def get(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_obj = user.objects.get(email=email,password=password)
            serializer = UserSerializer(user_obj, partial=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return JsonResponse({'message': 'Invalid email or password.'}, status=401)
class GetuserinfoAPIView(APIView):
    def get(self,request,id):
        try:
            user.objects.get(id=id)
            return Response(data="Account exist", status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return JsonResponse({'message': 'Account does not exist'}, status=401)
class GetCustomerExistAPIView(APIView):
    def get(self,request,uid):
        try:
            customer.objects.get(uid=uid)
            return Response(data="Customer exist", status=status.HTTP_200_OK)
        except customer.DoesNotExist:
            return JsonResponse({'message': 'Customer does not exist'}, status=401)
class GetCustomerinfoAPIView(APIView):
    def get(self,request,uid):
        try:
            customer_obj=customer.objects.get(uid=uid)
            serializer=CustomerSerializer(customer_obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except customer.DoesNotExist:
            return JsonResponse({'message': 'Customer does not exist'}, status=401)
class UpdateUserAPIView(APIView):
    def patch(self, request, id):
        try:
            user_obj = user.objects.get(id=id)
        except user.DoesNotExist:
            return Response(data={"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateCustomerAPIView(APIView):
    def patch(self, request, uid):
        try:
            customer_obj = customer.objects.get(uid=uid)
        except customer.DoesNotExist:
            return Response(data={"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisAPIView(APIView):
    def post(self, request):
        try:
            user.objects.get(email=request.data.get('email'))
            return Response(data="Account already exists.", status=status.HTTP_400_BAD_REQUEST)
        except user.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteUserAPIView(APIView):

    def delete(self, request, id):
        try:
            user_obj = user.objects.get(id=id)
        except user.DoesNotExist:
            return Response({'detail': f'User with id {id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        user_obj.delete()
        return Response({'detail': f'User with id {id} has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
class RegisCustomerAPIView(APIView):
    def post(self, request):
        try:
            customer.objects.get(uid=request.data.get('uid'))
            return Response(data="Customer already exists.", status=status.HTTP_400_BAD_REQUEST)
        except customer.DoesNotExist:
            try:
                user.objects.get(id=request.data.get('uid'))
                serializer = CustomerSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except user.DoesNotExist:
                return Response(data="User does not exist", status=status.HTTP_400_BAD_REQUEST)

