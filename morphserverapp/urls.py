from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('contacts',views.contacts, name='contacts'),
    path('help',views.morph_help, name='help'),
    path('user/sign_up',views.sign_up, name='sign_up'),
    path('user/sign_in',views.sign_in,name='sign_in'),
    path('user/sign_out', views.sign_out, name='sign_out'),
    path('user/reset_password',views.reset_password, name='reset_password'),
    re_path(r'^user/new_password/', views.new_password, name='new_password'),
    path('history',views.history,name='history'),
    path('morph/archive',views.archive, name='archive'),
    path('morph/new',views.new_morph,name='new_morph'),
    path('morph/<int:mr_id>',views.morph_request,name='morph_request'),

]