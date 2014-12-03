import os
import json
import fnmatch
import random
import string
from PIL import Image
import datetime
import exifread

import pprint

from dateutil.parser import parse
from django.http import HttpResponse

from pytz import utc
from background.models import BackgroundImage

from mediapanel import settings
from mediapanel.settings import BASE_DIR


def index(request):
    random_background = BackgroundImage.objects.all().order_by('?')[0]

    response_data = {}
    response_data['path'] = random_background.path

    response_data['album'] = random_background.album
    response_data['taken_by'] = random_background.taken_by
    response_data['date_taken'] = str(random_background.date_taken)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def gather_images(request):
    print 'Gathering images'

    pp = pprint.PrettyPrinter(indent=4)

    base_path = os.path.join(BASE_DIR, 'mediapanel', settings.STATICFILES_DIRS[0])
    for dir_path, dir_names, file_names in os.walk(base_path, followlinks=True):
        for filename in filter(is_image_file, file_names):
            image_path = os.path.join(dir_path, filename)

            """image_file = open(image_path, 'rb')
            exif_tags = exifread.process_file(image_file, stop_tag='EXIF DateTimeOriginal')

            date_taken = exif_tags['EXIF DateTimeOriginal']
            print pp.pprint(date_taken)"""

            #minimum_creation_time = get_minimum_creation_time(exif_data)
            #minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())
            #if minimum_creation_time is None:
            #    date_taken = datetime.datetime.now().replace(tzinfo=utc)
            #else:
            #    date_taken = parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)

            try:
                if Image.open(image_path)._getexif() is None:
                    date_taken = datetime.datetime.now().replace(tzinfo=utc)
                else:
                    minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())

                    if minimum_creation_time is None:
                        date_taken = datetime.datetime.now().replace(tzinfo=utc)
                    else:
                        date_taken = parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
            except AttributeError:
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AttributeError"

            taken_by = None
            image_path = os.path.join(os.path.relpath(dir_path, base_path), filename).replace("\\", "/")
            image_data = image_path.split(os.path.altsep)

            #print 'ID:', image_data

            album = image_data[-2]

            if len(image_data) > 2:
                taken_by = image_data[-2]
                album = string.join(image_data[:-2], ' / ')

            if BackgroundImage.objects.filter(path=image_path).count() == 0:
                print 'BackgroundImage > add object', image_data

                BackgroundImage(
                    path=image_path,
                    album=album,
                    taken_by=taken_by,
                    date_taken=date_taken
                ).save()

    print "BackgroundImage.objects.size(): " + str(BackgroundImage.objects.all().count())
    return HttpResponse()


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