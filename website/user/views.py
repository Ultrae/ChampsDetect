from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_exempt

import zipfile

from .forms import UserForm

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the folder
            img_zip = zipfile.ZipFile(request.FILES['img_folder'])
            img_zip.extractall('zip_folders/')
            img_zip.close()

            return render(request, 'user/index.html')
    else:
        form = UserForm()
    return render(request, 'user/index.html', { 'form': form })