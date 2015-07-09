from django.shortcuts import render
from api.models import Entry, ApiKey
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q

from keyvalue.utility import create_api_key

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
    key_root = request.user.apikey_set.get(is_key_root=True)
    key_generate = request.user.apikey_set.get(is_key_generate=True)
    keys = request.user.apikey_set.filter(is_key_root=None, is_key_generate=None).order_by('created_time')
    return render(request, 'control/management/apikeys.html', {'active': 'apikeys',
                                                               'keys': keys,
                                                               'key_root': key_root,
                                                               'key_generate': key_generate
                                                               })


''' Settings '''
@login_required
def restrictions(request):
    return render(request, 'control/settings/restrictions.html', {'active': 'restrictions'})


''' Form submits '''
@login_required
def generate_apikey(request):
    if request.method == 'POST':
        create_api_key(request.user, request)

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


