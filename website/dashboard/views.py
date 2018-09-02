from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from user.models import Log


def index(request):
    data = Log.objects.all()
    return render(request, 'dashboard/index.html', {'data': data})
