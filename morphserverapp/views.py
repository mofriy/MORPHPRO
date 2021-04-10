from django.http import HttpResponse, Http404
from django.template import loader
from .models import MorphRequest

# Create your views here.

def home(request):
    template = loader.get_template('morphserverapp/home.html')
    return HttpResponse(template.render())


def about(request):
    template = loader.get_template('morphserverapp/about.html')
    return HttpResponse(template.render())


def contacts(request):
    template = loader.get_template('morphserverapp/contacts.html')
    return HttpResponse(template.render())


def help(request):
    template = loader.get_template('morphserverapp/help.html')
    return HttpResponse(template.render())