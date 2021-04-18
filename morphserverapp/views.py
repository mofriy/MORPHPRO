from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User,MorphRequest,Pdb
from django.contrib.auth import hashers
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail
from django.contrib import messages
import datetime
# Create your views here.


def home(request):
    template = loader.get_template('morphserverapp/home.html')
    return HttpResponse(template.render({'user_greeting':request.session.get('name')},request))

def about(request):
    template = loader.get_template('morphserverapp/about.html')
    return HttpResponse(template.render({'user_greeting':request.session.get('name')},request))


def contacts(request):
    template = loader.get_template('morphserverapp/contacts.html')
    return HttpResponse(template.render({'user_greeting':request.session.get('name')},request))


def morph_help(request):
    template = loader.get_template('morphserverapp/help.html')
    return HttpResponse(template.render({'user_greeting':request.session.get('name')},request))



def sign_up(request):

    sign_up_template = loader.get_template('morphserverapp/sign_up.html')

    if request.method == 'POST':

        #awful
        if request.POST.get('password') != request.POST.get('password_confirmation'):
            messages.add_message(request, messages.ERROR, 'Passwords do not match!')
            return HttpResponseRedirect('./sign_up')

        if len(request.POST.get('name')) == 0:
            messages.add_message(request, messages.ERROR, 'Please enter name')
            return HttpResponseRedirect('./sign_up')

        if len(request.POST.get('email')) == 0:
            messages.add_message(request, messages.ERROR, 'Please enter email')
            return HttpResponseRedirect('./sign_up')

        #TODO: add more to this
        if request.POST.get('email').find('@') == -1:
            messages.add_message(request, messages.ERROR, 'Invalid email!')
            return HttpResponseRedirect('./sign_up')

        #TODO: add more to this
        if len(request.POST.get('password')) < 6:
            messages.add_message(request, messages.ERROR, 'Password is too short, minimal length - 6 characters')
            return HttpResponseRedirect('./sign_up')



        new_user = User.create_user({'name': request.POST.get('name'), 'email': request.POST.get('email'),
                                     'password': hashers.make_password(request.POST.get('password'))})
        new_user.save()

        request.session['name'] = new_user.name
        request.session['user_id'] = new_user.pk
        request.session.set_expiry(0)

        messages.add_message(request,messages.SUCCESS,'Registration successful!')

        return HttpResponseRedirect('../')

    return HttpResponse(sign_up_template.render(request=request))


def sign_in(request):

    sign_in_template = loader.get_template('morphserverapp/sign_in.html')

    if request.method == 'POST':
        # password check
        input_email = request.POST.get('email')

        try:
            found_user = User.objects.get(email=input_email)
        except User.DoesNotExist:
            messages.add_message(request,messages.ERROR,'User with this email does not exist')
            return HttpResponseRedirect('./sign_in')
        if not hashers.check_password(request.POST.get('password'), found_user.password):
            messages.add_message(request,messages.ERROR,'Wrong password!')
            return HttpResponseRedirect('./sign_in')

        request.session['name'] = found_user.name
        request.session['user_id'] = found_user.pk

        if request.POST.get('remember_me'):
            # TODO: NOTE! this is an example of lazyness, needs rework
            request.session.set_expiry(2592000)
        else:
            request.session.set_expiry(0)

        messages.add_message(request,messages.SUCCESS,'Signed in successfuly!')

        return HttpResponseRedirect('../')

    return HttpResponse(sign_in_template.render(request=request))


def sign_out(request):
    del request.session['name']
    del request.session['user_id']
    return HttpResponseRedirect('../')


def reset_password(request):
    reset_password_template = loader.get_template('morphserverapp/reset_password.html')
    if request.method == 'POST':

        try:
            found_user=User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            messages.add_message(request,messages.ERROR,'User with this email does not exist')
            return HttpResponseRedirect('./reset_password')

        #TODO: this code written only for development!!! everything here needs rework
        user_upd_token = urlsafe_base64_encode(force_bytes(found_user.user_updated_at))
        link = 'http://127.0.0.1:8000/user/new_password/?var=' + str(user_upd_token)
        send_mail(subject='MORPHPRO password recovery',message='Click on the following link, and choose a new passord: \n'+ link
                  ,from_email=None,recipient_list=[found_user.email],fail_silently=True)

        #TODO dev!!!
        print(link)

        messages.add_message(request,messages.SUCCESS,'Instructions were sent to your email.')

        return HttpResponseRedirect('../')

    return HttpResponse(reset_password_template.render(request=request))


def new_password(request):
    new_password_template = loader.get_template('morphserverapp/new_password.html')
    if request.method == 'POST':

        if request.POST.get('password') != request.POST.get('password_confirmation'):
            messages.add_message(request, messages.ERROR, 'Passwords do not match!')
            return HttpResponseRedirect('./?var='+request.session.get('encoded_time'))

        if len(request.POST.get('password')) < 6:
            messages.add_message(request, messages.ERROR, 'Password is too short, minimal length - 6 characters')
            return HttpResponseRedirect('./?var='+request.session.get('encoded_time'))

        try:
            uua = urlsafe_base64_decode(request.session.get('encoded_time'))
            uua_str = force_str(uua)
            upd_date = datetime.datetime.strptime(uua_str,'%Y-%m-%d %H:%M:%S.%f')
            found_user=User.objects.get(user_updated_at=upd_date)
        except User.DoesNotExist:
            return HttpResponseRedirect('./reset_password')


        found_user.password = hashers.make_password(request.POST.get('password'))
        found_user.user_updated_at = datetime.datetime.now()
        found_user.save()

        request.session['name'] = found_user.name
        request.session['user_id'] = found_user.pk
        del request.session['encoded_time']

        if request.POST.get('remember_me'):
            request.session.set_expiry(2592000)
        else:
            request.session.set_expiry(0)

        messages.add_message(request,messages.SUCCESS,'Password was successfuly changed!')

        return HttpResponseRedirect('../')

    request.session['encoded_time'] = request.GET.get('var')
    return HttpResponse(new_password_template.render(request=request))


def archive(request):
    archive_template = loader.get_template('morphserverapp/archive.html')
    all_mr_table = []

    for mr in MorphRequest.objects.all():
        try:
            author = User.objects.get(pk=mr.author)
        except User.DoesNotExist:
            return HttpResponseRedirect('../')
        all_mr_table.append([str(author.name),str(mr.created_at)[:len(str(mr.created_at))-7],str(mr.protein_a_name),str(mr.protein_b_name),
                         str(mr.morphing_count),'/morph/'+str(mr.id)])
    return HttpResponse(archive_template.render({'morph_requests':all_mr_table,'user_greeting':request.session.get('name')},request))


def history(request):
    my_request_template = loader.get_template('morphserverapp/history.html')
    my_mr_table = []
    for mr in MorphRequest.objects.all():
        if mr.author == request.session.get('user_id'):
            my_mr_table.append([str(mr.created_at)[:len(str(mr.created_at)) - 7], str(mr.protein_a_name),
                 str(mr.protein_b_name), str(mr.morphing_count), '/morph/' + str(mr.id)])
    return HttpResponse(my_request_template.render({'morph_requests': my_mr_table, 'user_greeting': request.session.get('name')},request))


def new_morph(request):
    morph_template = loader.get_template('morphserverapp/morph.html')
    if request.method == 'POST':

        pr_a_name = request.POST.get('protein_a_name')
        pr_b_name = request.POST.get('protein_b_name')
        if len(Pdb.objects.filter(pdb_name=pr_a_name)) == 0:
            pdb1= Pdb.create_pdb(pr_a_name,request.POST.get('protein_a'))
            pdb1.save()
        if len(Pdb.objects.filter(pdb_name=pr_b_name)) == 0:
            pdb2 = Pdb.create_pdb(pr_b_name,request.POST.get('protein_b'))
            pdb2.save()

        uid = request.session.get('user_id')
        if not uid:
           uid = 0

        morph_request_new = MorphRequest.create_request({'protein_a_name':pr_a_name,'protein_b_name':pr_b_name,'author':uid,
                                                     'morphing_count':request.POST.get('morphing_count'),
                                                     'auto_interpolation':request.POST.get('auto_interpolation')})

        morph_request_new.save()


        return HttpResponseRedirect('./'+str(morph_request_new.pk))

    return HttpResponse(morph_template.render({'user_greeting':request.session.get('name')},request))


def morph_request(request,mr_id):
    morph_request_template = loader.get_template('morphserverapp/morph_request.html')
    try:
        mr = MorphRequest.objects.get(pk=mr_id)
        submitter = User.objects.get(pk=mr.author)
    except MorphRequest.DoesNotExist or User.DoesNotExist:
        return HttpResponseRedirect('../')

    return HttpResponse(morph_request_template.render({'user_greeting':request.session.get('name'),
                                                       'morph_request':mr,'submitter':submitter.name},request))



