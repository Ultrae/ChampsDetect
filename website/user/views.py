from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from .forms import UserForm
from user.models import Log

import zipfile
import sys
import os
import datetime
from PIL import Image, ImageDraw

sys.path.insert(0, '../IA/')
from reconnaissance import *

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the folder
            if not os.path.exists("image_folder/"):
                os.makedirs("image_folder")

            name = request.FILES['img_folder'].name
            zip = int(form['type_of_picture'].data) == 1
            png = int(form['type_of_picture'].data) == 2
            if zip: # zip
                try:
                    name = zipSaving(request)
                except zipfile.BadZipFile:
                    return render(request, 'user/index.html',
                                    {'form': form})
                # Call hyperspectr
            elif png: # PNG
                classicPictureSaving(request)

            # Cut in little pieces
            '''path = 'image_folder/' + name + "/"
            new_dir = 'cut_images/' + name + "/"
            for file in os.listdir(path):
                new_new_dir =  new_dir + file
                if int(form['type_of_picture'].data) == 1:
                    cut(path + file, new_new_dir)
                elif png:
                    cut_jpg_png(path + file, new_new_dir)'''

            # Recognition
            # List of int
            result = []
            if zip:
                result = recognize("../IA/model.h5", new_dir + "478nm.tiff")
            elif png:
                result = recognize("../IA/model.h5", new_dir + "/" + name)
            anomaly_rate = (len(result) / 400) * 100

            # Build the picture
            dir_save = "result_color"
            if not os.path.exists("static/" + dir_save):
                os.makedirs("static/" + dir_save)
            img = None
            if zip:
                img = color(path + "610nm.tiff", path + "550nm.tiff", path + "466nm.tiff")
            else:
                img = Image.open(path + name)
            img = img.convert("RGB")

            # Show anomalies on the picture
            filepath = showAnomalies(dir_save, img, result)

            log = Log(date=datetime.datetime.now(),
                      description=form['select'].data,
                      pourcent=round(anomaly_rate))
            log.save()

            return render(request, 'user/index.html', { 'img': filepath,
                                                        'rate': anomaly_rate
                                                        })
    else:
        form = UserForm()
    return render(request, 'user/index.html', { 'form': form })


def showAnomalies(saving_dir, img, recognition_result):
    inc = 0
    piece = 0
    result_len = len(recognition_result)
    for j in range(0, SIZE_IMG, SIZE_CELL):
        for i in range(0, SIZE_IMG, SIZE_CELL):
            if inc < result_len and recognition_result[inc] == piece:
                draw = ImageDraw.Draw(img)
                draw.rectangle([(i, j),
                                (i + SIZE_CELL, j + SIZE_CELL)],
                               outline="#ff0000")
                inc += 1
            piece += 1
    filepath = saving_dir + "/recognition.png"
    img.save("static/" + filepath)

    return filepath


def zipSaving(request):
    img_zip = zipfile.ZipFile(request.FILES['img_folder'])
    img_zip.extractall('image_folder/')
    name = img_zip.filename[:-4]
    img_zip.close()

    return name


def classicPictureSaving(request):
    name = request.FILES['img_folder'].name
    file = request.FILES['img_folder']
    if not os.path.exists("image_folder/" + name):
        os.makedirs("image_folder/" + name)
    with open('image_folder/' + name + "/" + name, "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    return name


def hyperspectralHandler(request):
    name = zipSaving(request)

    path = 'image_folder/' + name + "/"
    new_dir = 'cut_images/' + name + "/"
    for file in os.listdir(path):
        new_new_dir = new_dir + file
        cut(path + file, new_new_dir)

    img = None

    return img


def classicPictureHandler(request):
    name = classicPictureSaving(request)

    path = 'image_folder/' + name + "/"
    new_dir = 'cut_images/' + name + "/"
    for file in os.listdir(path):
        new_new_dir = new_dir + file
        cut_jpg_png(path + file, new_new_dir)

    img = None

    return img