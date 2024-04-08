from django.contrib import admin
from django.urls import path, include
from .views import *
# router.register(r'users', UserViewSet, basename="userss")
urlpatterns = [
     path("",home, name="home" ),
      path("user/",UserViewSet.as_view()),
      path("register/",Register.as_view()),
      path("referrals/", ReferralList.as_view()),
      path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
      
      
]
