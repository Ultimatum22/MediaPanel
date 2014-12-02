from django.shortcuts import render

# Screen dimensions: 1366 x 768
def index(request):
    return render(request, 'panel/index.html')
