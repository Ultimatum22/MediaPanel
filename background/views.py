import os
import json
import random
import string
from PIL import Image
import datetime
import dateutil

from django.http import HttpResponse
import shutil
from pytz import utc

from mediapanel import settings
from mediapanel.settings import BASE_DIR

all_photos = []
downloaded_photos = []
tmp_directory = os.path.join('MediaPanel', 'tmp')


def index(request):
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)

    print 'len(downloaded_photos)1 >> ', len(downloaded_photos)

    random_photo = random.choice(downloaded_photos)
    downloaded_photos.remove(random_photo)

    print 'len(downloaded_photos)2 >> ', len(downloaded_photos)

    return HttpResponse(json.dumps(get_photo_info(random_photo)), content_type="application/json")


def update(request):
    print "update background"
    flatten_folder_tree()
    print 'all_photos ', len(all_photos)
    grab_random_photos(12)
    print 'downloaded_photos ', len(downloaded_photos)

    return HttpResponse(None)


def grab_random_photos(number):
    if len(downloaded_photos) < 10:
        for i in range(0, number):
            image_path = random.choice(all_photos)

            head, tail = os.path.split(image_path)

            random_photo_path = os.path.join(tmp_directory, os.path.relpath(head))
            random_photo_file = os.path.join(random_photo_path, tail)

            if not os.path.exists(random_photo_path):
                os.makedirs(random_photo_path)

            shutil.copy2(image_path, random_photo_file)

            try:
                image = Image.open(random_photo_file)

                width = 2048
                height = int(float(image.size[1]) * float(width / float(image.size[0])))

                image.thumbnail((width, height), Image.ANTIALIAS)
                image.save(random_photo_file, "JPEG")
            except IOError:
                print "cannot create thumbnail for '%s'" % random_photo_file

            downloaded_photos.append(random_photo_file)


def flatten_folder_tree():
    base_path = os.path.join(BASE_DIR, settings.STATICFILES_DIRS[0])
    print 'flatten_folder_tree > base_path > ', base_path
    for dir_path, dir_names, file_names in os.walk(base_path, followlinks=True):
        for filename in filter(is_image_file, file_names):
            # print '>>: ', os.path.join(dir_path, filename)
            all_photos.append(os.path.join(dir_path, filename))


def get_photo_info(image_path):
    image_path = image_path.replace("\\", "/")

    album = ""
    taken_by = None
    image_data = image_path.split("/")

    date_taken = datetime.datetime.now().replace(tzinfo=utc)
    try:
        if Image.open(image_path)._getexif() is not None:
            creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())

            if creation_time is None:
                date_taken = 0
            else:
                date_taken = dateutil.parse(creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
    except AttributeError:
        pass # Do nothing if no date was in the photo property

    image_data = image_data[3:]  # Strip first 3 elements off the aray

    print 'image_data: ', len(image_data)
    print 'image_data: ', image_data

    response_data = {}
    # if len(image_data) > 2:
    #     taken_by = image_data[-2]
    #     album = string.join(image_data[3:-1], ' / ')
    #
    # response_data['path'] = image_path
    # response_data['album'] = album
    # response_data['taken_by'] = taken_by
    # response_data['date_taken'] = str(date_taken)

    response_data['path'] = image_path

    image_data_length = len(image_data)
    if image_data_length >= 2:
        album = image_data[-3]

    if image_data_length >= 3:
        taken_by = image_data[-2]

    if image_data_length >= 4:
        album = string.join(image_data[:-2], ' / ')

    response_data['album'] = album
    response_data['taken_by'] = taken_by
    response_data['date_taken'] = str(date_taken)









    # taken_by = None
    #     if Image.open(image_path)._getexif() is not None:
    #         minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())
    #
    #         if minimum_creation_time is None:
    #             date_taken = datetime.datetime.now().replace(tzinfo=utc)
    #         else:
    #             date_taken = dateutil.parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
    # except AttributeError:
    #     print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AttributeError"
    #
    # taken_by = None
    # # image_path = image_path.replace("\\", "/")
    # # image_data = image_path.split(os.path.altsep)
    #
    # print 'image_data: ', len(image_data)
    # print 'image_data1: ', image_data[:-2]
    # if len(image_data) > 2:
    #     taken_by = image_data[-2]
    #     album = string.join(image_data[3:-1], ' / ')
    #
    # response_data['path'] = image_path
    # response_data['album'] = album
    # response_data['taken_by'] = taken_by
    # response_data['date_taken'] = str(date_taken)
    #
    # print 'image_path: ', image_path

    # os.remove(image_path)

    return response_data


def get_minimum_creation_time(exif_data):
    creation_time = "?"
    if 306 in exif_data and exif_data[306] < creation_time: # 306 = DateTime
        creation_time = exif_data[306]
    if 36867 in exif_data and exif_data[36867] < creation_time:  # 36867 = DateTimeOriginal
        creation_time = exif_data[36867]
    if 36868 in exif_data and exif_data[36868] < creation_time:  # 36868 = DateTimeDigitized
        creation_time = exif_data[36868]

    return creation_time


def is_image_file(filename, extensions=['.jpg', '.jpeg', '.gif', '.png']):
    return any(filename.lower().endswith(e) for e in extensions)
