from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from .forms import UserForm

def index(request):
    return render(request, 'user/index.html')

def get_name(request):
    if request.method == 'POST':
        print("IF")
        form = UserForm(request.POST)
        if form.is_valid():
            return render(request, 'user/index.html')
    else:

        print("ELSE")
        form = UserForm()
    return render(request, 'user/index.html', {'form': form})