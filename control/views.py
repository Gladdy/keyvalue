from django.shortcuts import render
from api.models import Entry, ApiKey
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
import string
import random

@login_required
def index(request):
    return render(request, 'control/control.html')


''' Management '''
@login_required
def values(request):
    entries = Entry.objects.all()
    return render(request, 'control/management/values.html', {'active': 'values', 'entries': entries})

@login_required
def manual(request):
    return render(request, 'control/management/manual.html', {'active': 'manual'})

@login_required
def bulk(request):
    return render(request, 'control/management/bulk.html', {'active': 'bulk'})

@login_required
def apikeys(request):
    keys = request.user.apikey_set.all()
    return render(request, 'control/management/apikeys.html', {'active': 'apikeys', 'keys': keys})


''' Settings '''
@login_required
def restrictions(request):
    return render(request, 'control/settings/restrictions.html', {'active': 'restrictions'})

''' Utility '''
def randomstring(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

@login_required
def generate_apikey(request):

    if request.method == 'POST':

        try:
            ApiKey.objects.create(key=randomstring(16), user=request.user)
        except Exception:
            pass

    return redirect('control:apikeys')

@login_required
def delete_apikey(request):

    if request.method == 'POST':

        try:
            key = ApiKey.objects.get(key=request.POST['key'], user=request.user)
            key.delete()
        except ApiKey.DoesNotExist:
            pass

    return redirect('control:apikeys')


