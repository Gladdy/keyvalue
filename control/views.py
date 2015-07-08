from django.shortcuts import render
from api.models import Entry

def manage(request):
    entries = Entry.objects.filter()
    return render(request, 'control/manage.html')

def settings(request):
    return render(request, 'control/settings.html')