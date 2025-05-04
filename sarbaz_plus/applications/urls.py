from django.contrib import admin
from django.urls import path, include
from .views import CreateApplicationView


urlpatterns = [
    path('create/', CreateApplicationView.as_view(), name='create-application')
]