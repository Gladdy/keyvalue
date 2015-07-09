from django.contrib.auth import authenticate, login as django_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import IntegrityError
from api.models import ApiKey

from keyvalue.utility import create_api_key

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
        return render(request, "keyvalue/login.html", {'nextpage': request.GET.get('next', '/')})

    else:
        ''' Validate the credentials '''
        if 'id' in request.POST and 'password' in request.POST:
            identifier = request.POST['id']
            password = request.POST['password']
        else:
            return render(request, "keyvalue/login.html", {'error': "Please fill in all fields"})

        # Search for the username and email address to determine the user to log in
        candidates = User.objects.filter(Q(username=identifier)|Q(email=identifier))

        if candidates.count() == 0:
            return render(request, "keyvalue/login.html", {'error': "Unable to find username or email address"})

        candidate = candidates[0]

        # Try to authenticate the user
        user = authenticate(username=candidate.username, password=password)

        if user is not None:
            # If the password matches, log the user in
            django_login(request, user)

            # Extract the page that has been supplied for redirection
            return HttpResponseRedirect(request.POST.get('nextpage',''))
        else:
            return render(request, "keyvalue/login.html", {'error': "Invalid password"})


def register(request):

    if request.method == 'GET':
        ''' Show the registration page '''
        return render(request, "keyvalue/register.html")

    else:
        if 'username' in request.POST and 'email' in request.POST and \
                'password1' in request.POST and 'password2' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        else:
            return render(request, "keyvalue/register.html", {'error': "Please fill in all fields"})

        if password1 != password2:
            return render(request, "keyvalue/register.html", {'error': "The passwords do not match"})

        try:
            # Create the new account
            user = User.objects.create_user(username=username, email=email, password=password1)
            setup_new_user(user)

            # Log the new account in
            user = authenticate(username=username,password=password1)
            django_login(request, user)

            return render(request, "keyvalue/register.html", {'success': "Registration successful!"})

        except IntegrityError:
            return render(request, "keyvalue/register.html", {'error': "This username was already taken or invalid"})
        except Exception:
            return render(request, "keyvalue/register.html", {'error': "An error occurred: invalid data?"})

def setup_new_user(user):
    create_api_key(user, None, is_key_root=True)
    create_api_key(user, None, is_key_generate=True)
