from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    return render(request, 'expert/index.html')

def expert(request):
    return render(request, 'expert/expert.html')