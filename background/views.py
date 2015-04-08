import os
import json
import random
import shutil
import string
from PIL import Image
import datetime
import PIL
from dateutil.parser import parse

from django.http import HttpResponse
from pytz import utc

from background.models import BackgroundImage

from mediapanel import settings
from mediapanel.settings import BASE_DIR

all_photos = []
downloaded_photos = []
tmp_directory = os.path.join(BASE_DIR, 'mediapanel', 'tmp')


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
    # if len(downloaded_photos) < 10:
        for i in range(0, number):
            image_path = random.choice(all_photos)

            head, tail = os.path.split(image_path)

            print 'rel head: ', os.path.relpath(head)
            print 'tmp_directory: ', tmp_directory

            random_photo = os.path.join(tmp_directory, os.path.relpath(head), tail)

            if not os.path.exists(os.path.join(tmp_directory, os.path.relpath(head))):
                os.makedirs(os.path.join(tmp_directory, os.path.relpath(head)))

            shutil.copy2(image_path, random_photo)
            #
            # print 'image_path: ', image_path
            print 'random_photo: ', random_photo

            # try:
            #     size = 1920, 1080
            #     im = Image.open(image_path)
            #     im.thumbnail(size, Image.ANTIALIAS)
            #     im.save(random_photo, "JPEG")
            # except IOError:
            #     print "cannot create thumbnail for '%s'" % random_photo


            # basewidth = 1920
            # image = Image.open(random_photo)
            # wpercent = (basewidth/float(image.size[0]))
            # hsize = int((float(image.size[1])*float(wpercent)))
            # image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
            # image.save(random_photo)

            # size = 1920
            # image = Image.open(random_photo)
            # wpercent = (size/float(image.size[0]))
            # hsize = int((float(image.size[1])*float(wpercent)))
            # image.thumbnail(size,hsize, Image.ANTIALIAS)
            # image.save(random_photo, "JPEG")

            downloaded_photos.append(random_photo)


def flatten_folder_tree():
    base_path = os.path.join(BASE_DIR, 'mediapanel', settings.STATICFILES_DIRS[0])
    for dir_path, dir_names, file_names in os.walk(base_path, followlinks=True):
        for filename in filter(is_image_file, file_names):
            all_photos.append(os.path.join(dir_path, filename))


def get_photo_info(image_path1):
    taken_by = None
    image_path = os.path.relpath(image_path1).replace("\\", "/")
    image_data = image_path.split(os.path.altsep)

    response_data = {}
    response_data['path'] = image_path
    # response_data['album'] = album
    # response_data['taken_by'] = taken_by
    # response_data['date_taken'] = str(date_taken)

    print 'image_path: ', image_path

    return response_data



    #print 'image_path: ' + image_path

    # try:
    #     if Image.open(image_path)._getexif() is None:
    #         date_taken = datetime.datetime.now().replace(tzinfo=utc)
    #     else:
    #         minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())
    #
    #         if minimum_creation_time is None:
    #             date_taken = datetime.datetime.now().replace(tzinfo=utc)
    #         else:
    #             date_taken = parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
    # except AttributeError:
    #     print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AttributeError"
    #
    # taken_by = None
    # #image_path = image_path.replace("\\", "/")
    # image_path = image_path.replace("\\", "/")
    # #image_path = image_path.replace("\\", "/")
    # image_data = image_path.split(os.path.altsep)
    #
    # album = image_data[-2]
    #
    # if len(image_data) > 2:
    #     taken_by = image_data[-2]
    #     album = string.join(image_data[:-2], ' / ')
    #
    # response_data = {}
    # response_data['path'] = image_path
    # response_data['album'] = album
    # response_data['taken_by'] = taken_by
    # response_data['date_taken'] = str(date_taken)
    #
    # print 'date_taken: ', response_data['taken_by']
    #
    # return response_data


# def move(destination, depth=None):
#     if not depth:
#         depth = []
#     for file_or_dir in os.listdir(os.path.join([destination] + depth, "\\")):
#         if os.path.isfile(file_or_dir):
#             shutil.move(file_or_dir, destination)
#         else:
#             move(destination, os.path.join(depth + [file_or_dir], "\\"))

# def gather_images(request):
#     print 'Gathering images'
#
#     pp = pprint.PrettyPrinter(indent=4)
#
#     base_path = os.path.join(BASE_DIR, 'mediapanel', settings.STATICFILES_DIRS[0])
#     for dir_path, dir_names, file_names in os.walk(base_path, followlinks=True):
#         for filename in filter(is_image_file, file_names):
#             image_path = os.path.join(dir_path, filename)
#
#             """image_file = open(image_path, 'rb')
#             exif_tags = exifread.process_file(image_file, stop_tag='EXIF DateTimeOriginal')
#
#             date_taken = exif_tags['EXIF DateTimeOriginal']
#             print pp.pprint(date_taken)"""
#
#             #minimum_creation_time = get_minimum_creation_time(exif_data)
#             #minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())
#             #if minimum_creation_time is None:
#             #    date_taken = datetime.datetime.now().replace(tzinfo=utc)
#             #else:
#             #    date_taken = parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
#
#             try:
#                 if Image.open(image_path)._getexif() is None:
#                     date_taken = datetime.datetime.now().replace(tzinfo=utc)
#                 else:
#                     minimum_creation_time = get_minimum_creation_time(Image.open(image_path)._getexif())
#
#                     if minimum_creation_time is None:
#                         date_taken = datetime.datetime.now().replace(tzinfo=utc)
#                     else:
#                         date_taken = parse(minimum_creation_time.replace(':', '-', 2)).replace(tzinfo=utc)
#             except AttributeError:
#                 print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AttributeError"
#
#             taken_by = None
#             image_path = os.path.join(os.path.relpath(dir_path, base_path), filename).replace("\\", "/")
#             image_data = image_path.split(os.path.altsep)
#
#             #print 'ID:', image_data
#
#             album = image_data[-2]
#
#             if len(image_data) > 2:
#                 taken_by = image_data[-2]
#                 album = string.join(image_data[:-2], ' / ')
#
#             if BackgroundImage.objects.filter(path=image_path).count() == 0:
#                 print 'BackgroundImage > add object', image_data
#
#                 BackgroundImage(
#                     path=image_path,
#                     album=album,
#                     taken_by=taken_by,
#                     date_taken=date_taken
#                 ).save()
#
#     print "BackgroundImage.objects.size(): " + str(BackgroundImage.objects.all().count())
#     return HttpResponse()


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