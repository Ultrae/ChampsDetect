from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from user.models import Log
from django.db.models import Avg

def index(request):
    data = Log.objects.all()
    data2 = Log.objects.all().aggregate(Avg('pourcent'))
    data2 = round(data2['pourcent__avg'])
    return render(request, 'dashboard/index.html',
                  {'data': data, 'data2': data2})
