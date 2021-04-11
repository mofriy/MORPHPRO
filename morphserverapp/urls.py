from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('contacts',views.contacts, name='contacts'),
    path('help',views.help, name='help'),
    path('user/sign_up',views.sign_up, name='sign_up'),
    path('user/sign_in',views.sign_in,name='sign_in')
]