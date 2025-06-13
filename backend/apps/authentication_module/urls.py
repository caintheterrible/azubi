from django.urls import path
from apps.authentication_module.views import register, login

urlpatterns=[
    path('register/', register),
    path('login/', login),
]