import os
from django.shortcuts import render

# Screen dimensions: 1366 x 768
def index(request):
    # tmp_directory = os.path.join('mediapanel', 'tmp', 'Photo albums')
    # for root, dirs, files in os.walk(tmp_directory, topdown=False):
    #     for name in files:
    #         os.remove(os.path.join(root, name))
    #     for name in dirs:
    #         os.rmdir(os.path.join(root, name))

    # shutil.rmtree(tmp_directory)

    return render(request, 'panel/index.html')
