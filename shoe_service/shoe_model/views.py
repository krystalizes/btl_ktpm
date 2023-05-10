from django.http import JsonResponse


# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import shoes
import requests
import json


from .serializers import ShoesSerializer


class GetAllShoesAPIView(APIView):
    def get(self,request):
        shoe=shoes.objects.all()
        if shoe:
            serializer = ShoesSerializer(shoe, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="No data available", status=status.HTTP_404_NOT_FOUND)
class GetshoeinfoAPIView(APIView):
    def get(self,request,id):
        try:
            shoe=shoes.objects.get(id=id)
            serializer = ShoesSerializer(shoe, partial=True)
            serialized_data = serializer.data
            serialized_data['status'] = 'Success'
            return Response(data=serialized_data, status=status.HTTP_200_OK)
        except shoes.DoesNotExist:
            return JsonResponse({'message': 'Shoe does not exist','status':'Failed'}, status=status.HTTP_404_NOT_FOUND)
class UpdateShoeAPIView(APIView):
    def patch(self, request, id):
        try:
            shoe_obj = shoes.objects.get(id=id)
        except shoes.DoesNotExist:
            return Response(data={"message": "Shoe not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShoesSerializer(shoe_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisShoeAPIView(APIView):
    def post(self, request):
        try:
            shoes.objects.get(id=request.data.get('id'))
            return Response(data="Shoe already exists.", status=status.HTTP_400_BAD_REQUEST)
        except shoes.DoesNotExist:
            serializer = ShoesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteShoeAPIView(APIView):

    def delete(self, request, id):
        try:
            shoe_obj = shoes.objects.get(id=id)
        except shoes.DoesNotExist:
            return Response({'detail': f'Shoe with id {id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        shoe_obj.delete()
        return Response({'detail': f'Shoe with id {id} has been deleted.'}, status=status.HTTP_204_NO_CONTENT)


