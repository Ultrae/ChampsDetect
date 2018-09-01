from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from .forms import UserForm

import zipfile
import sys
import os
import datetime
from PIL import Image
import numpy

sys.path.insert(0, '../IA/')

from reconnaissance import cut, recognize, color

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the folder
            name = zipHandler(request)

            # Cut in little pieces
            path = 'zip_folders/' + name + "/"
            new_dir = 'cut_images/' + name + "/"
            for file in os.listdir(path):
                new_new_dir =  new_dir + file
                cut(path + file, new_new_dir)

            # Recognition
            # List of int
            result = recognize("../IA/model.h5", new_dir + "466nm.tiff")
            print(result)

            # Build the picture
            dir_save = "result_color"
            if not os.path.exists("static/" + dir_save):
                os.makedirs("static/" + dir_save)
            img = color(path + "610nm.tiff", path + "550nm.tiff", path + "466nm.tiff")
            img = img.convert("RGB")
            filepath = dir_save + "/recognition.png"
            img.save("static/" + filepath)

            return render(request, 'user/index.html', { 'img': filepath })
    else:
        form = UserForm()
    return render(request, 'user/index.html', { 'form': form })


def zipHandler(request):
    img_zip = zipfile.ZipFile(request.FILES['img_folder'])
    img_zip.extractall('zip_folders/')
    name = img_zip.filename[:-4]
    img_zip.close()

    return name