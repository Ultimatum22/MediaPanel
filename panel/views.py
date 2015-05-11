from django.shortcuts import render
from django.http import HttpResponse

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


def barchart(request):

    #instantiate a drawing object
    d = mycharts.MyBarChartDrawing()

    #extract the request params of interest.
    #I suggest having a default for everything.
    if 'height' in request:
        d.height = int(request['height'])
    if 'width' in request:
        d.width = int(request['width'])

    if 'numbers' in request:
        strNumbers = request['numbers']
        numbers = map(int, strNumbers.split(','))
        d.chart.data = [numbers]   #bar charts take a list-of-lists for data

    if 'title' in request:
        d.title.text = request['title']


    #get a GIF (or PNG, JPG, or whatever)
    binaryStuff = d.asString('gif')
    return HttpResponse(binaryStuff, 'image/gif')


def linechart(request):

    #instantiate a drawing object
    d = mycharts.MyLineChartDrawing()

    #extract the request params of interest.
    #I suggest having a default for everything.


    d.height = 200
    d.chart.height = 159


    d.width = 300
    d.chart.width = 300

    d.title._text = request.session.get('Some custom title')



    d.XLabel._text = request.session.get('X Axis Labell')
    d.YLabel._text = request.session.get('Y Axis Label')

    d.chart.data = [((1,1), (2,2), (2.5,1), (3,3), (4,5)),((1,2), (2,3), (2.5,2), (3.5,5), (4,6))]



    labels =  ["Label One","Label Two"]
    if labels:
        # set colors in the legend
        d.Legend.colorNamePairs = []
        for cnt,label in enumerate(labels):
            d.Legend.colorNamePairs.append((d.chart.lines[cnt].strokeColor,label))


    #get a GIF (or PNG, JPG, or whatever)
    binaryStuff = d.asString('png')
    return HttpResponse(binaryStuff, 'image/png')