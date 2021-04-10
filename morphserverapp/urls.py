from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('contacts',views.contacts, name='contacts'),
    path('help',views.help, name='help'),
    #path('jsclient/<int:MorphRequest_id>'),
]