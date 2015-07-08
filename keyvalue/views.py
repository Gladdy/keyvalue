from django.contrib.auth import authenticate, login as django_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    if request.user.is_authenticated():
        return render(request, 'keyvalue/index-login.html')
    else:
        return render(request, 'keyvalue/index.html')


def features(request):
    return render(request, 'keyvalue/features.html')


def about(request):
    return render(request, 'keyvalue/about.html')


def login(request):

    if request.user.is_authenticated():
        ''' No need to show login page whenever the user is already logged in '''
        return redirect('index-index')

    elif request.method == 'GET':
        ''' Show the login page '''
        return render(request, "keyvalue/login.html")

    else:
        ''' Validate the credentials '''
        if 'id' in request.POST and 'password' in request.POST:
            identifier = request.POST['id']
            password = request.POST['password']
        else:
            return render(request, "keyvalue/login.html", {'error': "Please fill in all fields"})

        try:
            candidate = User.objects.get(Q(username=identifier)|Q(email=identifier))
        except User.DoesNotExist:
            return render(request, "keyvalue/login.html", {'error': "Unable to find username or email address"})

        user = authenticate(username=candidate.username, password=password)

        if user is not None:
            django_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, "keyvalue/login.html", {'error': "Invalid password"})


def register(request):

    if request.method == 'GET':
        ''' Show the registration page '''
        return render(request, "keyvalue/register.html")

    else:
        if 'username' in request.POST and \
                'email' in request.POST and \
                'password1' in request.POST and \
                'password2' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        else:
            return render(request, "keyvalue/register.html", {'error': "Please fill in all fields"})

        if password1 != password2:
            return render(request, "keyvalue/register.html", {'error': "The passwords do not match"})

        try:
            User.objects.create_user(username=username, email=email,password=password1)
            user = authenticate(username=username,password=password1)
            django_login(request,user)
            return render(request, "keyvalue/register.html", {'success': "Registration successful!"})

        except IntegrityError:
            return render(request, "keyvalue/register.html", {'error': "This username was already taken or invalid"})
        except Exception:
            return render(request, "keyvalue/register.html", {'error': "An error occurred: invalid data?"})
