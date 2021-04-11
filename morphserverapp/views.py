from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import MorphRequest,User
from .forms import RegistrationForm,SignInForm
from django.contrib.auth import hashers

# Create your views here.

def home(request):
    template = loader.get_template('morphserverapp/home.html')
    if request.session.get('name') != None and request.session.get('email') != None:
        return HttpResponse(template.render({'user_greeting':'Signed in as '+request.session.get('name')}))
    return HttpResponse(template.render({'user_greeting':'Not signed in'}))

def about(request):
    template = loader.get_template('morphserverapp/about.html')
    return HttpResponse(template.render({'user_greeting':'Signed in as '+request.session.get('name')}))


def contacts(request):
    template = loader.get_template('morphserverapp/contacts.html')
    return HttpResponse(template.render({'user_greeting':'Signed in as '+request.session.get('name')}))


def help(request):
    template = loader.get_template('morphserverapp/help.html')
    return HttpResponse(template.render({'user_greeting':'Signed in as '+request.session.get('name')}))



def sign_up(request):
    sign_up_template = loader.get_template('morphserverapp/sign_up.html')
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():

            new_user = User.create_user({'name':request.POST.get('name'),'email':request.POST.get('email'),
                                         'password':hashers.make_password(request.POST.get('password'))})

            if request.POST.get('password') != request.POST.get('password_validation'):
                registration_form = RegistrationForm()
                # TODO: this could be improved with message system
                return HttpResponseRedirect('./sign_up')

            new_user.save()

            request.session['name'] = new_user.name
            request.session['email'] = new_user.email
            request.session.set_expiry(0)
            return HttpResponseRedirect('../')
    else:
        registration_form = RegistrationForm()
    return HttpResponse(sign_up_template.render({'registration_form':registration_form},request))


def sign_in(request):
    sign_in_template = loader.get_template('morphserverapp/sign_in.html')
    if request.method == 'POST':
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():

            #password check
            input_email = request.POST.get('email')
            found_user = User.objects.get(email=input_email)
            if not hashers.check_password(request.POST.get('password'),found_user.password):
                sign_in_form = SignInForm()
                # TODO: this could be improved with message system
                return HttpResponseRedirect('./sign_in')

            request.session['name'] = found_user.name
            request.session['email'] = found_user.email
            if request.POST.get('remember_me'):
                #TODO: NOTE! this is an example of lazyness, needs rework
                request.session.set_expiry(2592000)
            else:
                request.session.set_expiry(0)
            return HttpResponseRedirect('../')
            # return HttpResponse(sign_in_success_template.render({'user_greeting':'Signed as'+found_user.name},request))
    else:
        sign_in_form = SignInForm()
    return HttpResponse(sign_in_template.render({'sign_in_form':sign_in_form},request))