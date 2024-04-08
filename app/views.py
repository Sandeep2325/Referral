from django.shortcuts import render
import datetime
from django.db.models import Count, Avg, Sum, Max, Min
from django.db.models import Q, F
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tokenverify import verify_and_extract_token_data
import json
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum items per page

# Create your views here.
@csrf_exempt
def home(request):
    if request.method=="GET":
       
        return JsonResponse({"message":True}) 
    name=request.POST
    return JsonResponse({"Post":name})

class UserViewSet(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def get(self, request, format=None):
        
        """
        Return a list of all users.
        """
        try:
            user_obj=User.objects.filter(id=request.user.id)
            serializer=UserSerializer(user_obj,many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            print("error in getting userlist", (e))
            return Response({"error":"Error getting user list"}, status=400)
    

class Register(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({"message": "Account created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":"Something went wrong","data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# class ReferralList(APIView):
#     permission_classes=(IsAuthenticated,)
#     authentication_classes=[JWTAuthentication,]
#     pagination_class = CustomPagination
#     def get(self, request, format=None):
        
#         """
#         Return a list of all users.
#         """
#         try:
#             user_obj=User.objects.filter(referredid=request.user.referid)
#             paginator = self.pagination_class()
#             result_page = paginator.paginate_queryset(user_obj, request)
#             serializer=UserSerializer(user_obj,many=True)
#             return paginator.get_paginated_response(serializer.data, status=200)
#             # return Response(serializer.data, status=200)
#         except Exception as e:
#             print("error in getting userlist", (e))
#             return Response({"error":"Error getting user list"}, status=400)
    
class ReferralList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]
    pagination_class = CustomPagination

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        try:
            user_obj = User.objects.filter(referredid=request.user.referid)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(user_obj, request)
            serializer = UserSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print("Error in getting user list:", e)
            return Response({"error": "Error getting user list"}, status=400)