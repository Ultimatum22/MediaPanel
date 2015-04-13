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

    random_photo = random.choice(downloaded_photos)
    return HttpResponse(json.dumps(get_photo_info(random_photo)), content_type="application/json")


def update(request):
    print "update background"
    flatten_folder_tree()
    print 'all_photos ', len(all_photos)
    grab_random_photos(10)
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
                size = 1920, 1080
                im = Image.open(random_photo_file)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(random_photo_file, "JPEG")
            except IOError:
                print "cannot create thumbnail for '%s'" % random_photo_file

            downloaded_photos.append(random_photo_file)


def flatten_folder_tree():
    base_path = os.path.join(BASE_DIR, settings.STATICFILES_DIRS[0])
    print 'flatten_folder_tree > base_path > ', base_path
    for dir_path, dir_names, file_names in os.walk(base_path, followlinks=True):
        for filename in filter(is_image_file, file_names):
            print '>>: ', os.path.join(dir_path, filename)
            all_photos.append(os.path.join(dir_path, filename))


def get_photo_info(image_path1):
    taken_by = None
    image_path = image_path1.replace("\\", "/")
    image_data = image_path.split(os.path.altsep)

    try:
        if Image.open(image_path)._getexif() is None:
            date_taken = datetime.datetime.now().replace(tzinfo=utc)
        else:
            minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())

            if minimum_creation_time is None:
                date_taken = datetime.datetime.now().replace(tzinfo=utc)
            else:
                date_taken = dateutil.parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
    except AttributeError:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AttributeError"

    taken_by = None
    image_path = image_path.replace("\\", "/")
    image_data = image_path.split(os.path.altsep)

    print 'image_data: ', len(image_data)
    print 'image_data1: ', image_data[:-2]
    if len(image_data) > 2:
        taken_by = image_data[-2]
        album = string.join(image_data[3:-1], ' / ')

    response_data = {}
    response_data['path'] = image_path
    response_data['album'] = album
    response_data['taken_by'] = taken_by
    response_data['date_taken'] = str(date_taken)

    print 'image_path: ', image_path

    # os.remove(image_path)

    return response_data


def get_minimum_creation_time(exif_data):
    mtime = "?"
    #if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
    #    mtime = exif_data[306]
    """if 'EXIF DateTimeOriginal' in exif_tags and exif_tags['EXIF DateTimeOriginal'] < mtime:  # 36867 = DateTimeOriginal
        mtime = exif_tags['EXIF DateTimeOriginal']
    if 'EXIF DateTimeDigitized' in exif_tags and exif_tags['EXIF DateTimeDigitized'] < mtime:  # 36868 = DateTimeDigitized
        mtime = exif_tags['EXIF DateTimeDigitized']
    return mtime"""

    mtime = "?"
    if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
        mtime = exif_data[306]
    if 36867 in exif_data and exif_data[36867] < mtime:  # 36867 = DateTimeOriginal
        mtime = exif_data[36867]
    if 36868 in exif_data and exif_data[36868] < mtime:  # 36868 = DateTimeDigitized
        mtime = exif_data[36868]
    return mtime


def is_image_file(filename, extensions=['.jpg', '.jpeg', '.gif', '.png']):
    return any(filename.lower().endswith(e) for e in extensions)