from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from .forms import UserForm

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            return render(request, 'user/index.html')
    else:
        form = UserForm()
    return render(request, 'user/index.html', {'form': form})