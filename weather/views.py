import json
import os
from urllib import quote, urlopen
from urllib2 import URLError
import configparser
from datetime import datetime

from django.http import HttpResponse
from mediapanel.settings import BASE_DIR

temp_file = os.path.join('MediaPanel', 'tmp', 'pywu.cache.json')
conf_file = os.path.join(BASE_DIR, 'weather', ".pywu.conf")


def index(request):
    pass


def forecast_10_days(request):
    api_key, location = get_api_data()

    base_url = "http://api.wunderground.com/api/%s" % api_key
    astronomy_url = base_url + "/astronomy/q/%s.json" % quote(location)
    forecast_10_days_url = base_url + "/conditions/forecast10day/q/%s.json" % quote(location)

    print "Fetching forecast for 10 days... ", forecast_10_days_url

    try:
        forecast_10_days_response = urlopen(forecast_10_days_url)
        astronomy_response = urlopen(astronomy_url)
    except URLError as e:
        if hasattr(e, 'reason'):
            print e.reason
        elif hasattr(e, 'code'):
            print "Status returned: " + str(e.code)

    astronomy_data = json.loads(astronomy_response.read().decode())
    ten_days_forecast_data = json.loads(forecast_10_days_response.read().decode())

    print 'astronomy_data: ', astronomy_data

    # Assign forecast to a dictionary
    forecast_dict = []

    try:
        ten_days_forecast = ten_days_forecast_data['forecast']['simpleforecast']['forecastday']
    except KeyError:
        print 'No Data'

    print "Data fetched successfully"

    sunset_time = astronomy_data['sun_phase']['sunset']['hour'] + ":" + astronomy_data['sun_phase']['sunset']['minute']
    sunrise_time = astronomy_data['sun_phase']['sunrise']['hour'] + ":" + astronomy_data['sun_phase']['sunrise']['minute']

    print 'datetime.datetime.now().time(): ', datetime.now().strftime('%H')

    weather_html = '<table style="width: 100%; border-top: 1px solid rgba(255,255,255,.1);"><tbody><tr>'
    weather_html += '<td style="padding: 0 20px 5px 20px; width: 250px;">'
    weather_html += '<div class="bright large">12<sup>&deg;</sup>'
    weather_html += '<span class="wi wi-day-sunny" style="font-size: 70px;" title="clear"></span>'
    weather_html += '</div>'

    weather_html += '<div style="margin-top: 15px;">'

    current_hour = datetime.now().strftime('%H')
    current_minute = datetime.now().strftime('%M')
    if (current_hour >= astronomy_data['sun_phase']['sunset']['hour'] and current_minute >= astronomy_data['sun_phase']['sunset']['minute']) and (current_hour < astronomy_data['sun_phase']['sunrise']['hour'] and current_minute < astronomy_data['sun_phase']['sunrise']['minute']):
        print 'Sunset'
        weather_html += '<span class="wi wi-strong-wind"></span> 7 wnw &nbsp;&nbsp;<span class="wi wi-sunset"></span> %s:%s</div>' % (astronomy_data['sun_phase']['sunset']['hour'], astronomy_data['sun_phase']['sunset']['minute'])
    else:
        print 'Sunrise'
        weather_html += '<span class="wi wi-strong-wind"></span> 7 wnw &nbsp;&nbsp;<span class="wi wi-sunrise"></span> %s:%s</div>' % (astronomy_data['sun_phase']['sunrise']['hour'], astronomy_data['sun_phase']['sunrise']['minute'])
    weather_html += '</td>'

    # count = 1

    # forecast_iter = enumerate(forecast)
    # forecast_iter.next();
    # for i, node in forecast_iter:
    for node in ten_days_forecast[:4]:
        date = node['date']

        weather_html += '<td style="padding: 5px 40px; text-align: center; border-left: 1px solid rgba(255,255,255,.1); line-height: 2em;">'
        weather_html += '<div class="day">' + date['weekday'] + '</div>'
        weather_html += '<span class="wi wi-day-cloudy bright medium"></span><br/>'
        weather_html += '<span class="bright" style="margin: 0 10px;">' + node['high']['celsius'] + '</span>'
        weather_html += '<span class="bright" style="margin: 0 10px;">' + node['low']['celsius'] + '</span></td>'

        # print 'Count: ', count
        # date = node['date']
        #
        # conditions = {
        #     'day': date['weekday'],
        #     'shortdate': str(date['day']) + '/' + str(date['month']) + '/' + str(date['year']),
        #     'longdate': str(date['day']) + ' ' + date['monthname'] + ', ' + str(date['year']),
        #     'low_c': node['low']['celsius'],
        #     'high_c': node['high']['celsius'],
        #     'condition': node['conditions'],
        #     'rain_mm': node['qpf_allday']['mm'],
        #     'snow_cm': node['snow_allday']['cm'],
        # }
        #
        # forecast_dict.append(conditions)
        # count += 1

    weather_html += '</tr></tbody></table>'

    return HttpResponse(weather_html)

    # return HttpResponse(json.dumps(forecast_dict), content_type="application/json")


def forecast_hourly_today(request):
    api_key, location = get_api_data()

    req = "http://api.wunderground.com/api/%s/hourly/q/" % api_key
    req += quote(location) + ".json"
    req += "astronomy/" + quote(location) + ".json"

    base_url = 'http://api.wunderground.com/api/%s/' % api_key
    condition_url = base_url + 'hourly/q/%s.json' % quote(location)
    astro_url = base_url + 'astronomy/q/%s.json' % quote(location)


    print "Fetching forecast hourly today... ", astro_url

    try:
        response = urlopen(astro_url)
    except URLError as e:
        if hasattr(e, 'reason'):
            print e.reason
        elif hasattr(e, 'code'):
            print "Status returned: " + str(e.code)

    json_data = response.read().decode()
    data = json.loads(json_data)

    print "Data fetched successfully"

    weather_html = '<table id="events_table"><tbody><tr>'


    weather_html += '</tr></tbody></table>'

    return HttpResponse(weather_html)

    # return HttpResponse(json.dumps(data), content_type="application/json")


def get_api_data():
    config = configparser.ConfigParser()
    config.read(conf_file)

    api_key = ""
    location = ""

    try:
        api_key = config['PYWU']['apikey']
        location = config['PYWU']['location']
    except KeyError:
        print 'Could not find data'

    return api_key, location

# def convert_icon(icon, current=False):
#
#     pattern = re.compile(r'[A-Za-z]+ \d+ (.+):\d+:\d+')
#     time_string = data['current_observation']['local_time_rfc822']
#     hour = int(pattern.search(time_string).group(1))
#
#     day_icon_dict = {
#         "chancerain"    : "g",
#         "sunny"         : "a",
#         "mostlysunny"   : "b",
#         "partlycloudy"  : "c",
#         "mostlycloudy"  : "d",
#         "rain"          : "i",
#         "chancesnow"    : "o",
#         "cloudy"        : "e",
#         "tstorms"       : "m",
#         "chancetstorms" : "k",
#         "sleet"         : "q",
#         "snow"          : "q",
#         "fog"           : "e",
#         "smoke"         : "e",
#         "hazy"          : "e",
#         "flurries"      : "p",
#         "chanceflurries": "o",
#         "chancesleet"   : "o",
#         "clear"         : "a",
#         "partlysunny"   : "c",
#         }
#
#     night_icon_dict = {
#         "chancerain"    : "G",
#         "sunny"         : "A",
#         "mostlysunny"   : "B",
#         "partlycloudy"  : "C",
#         "mostlycloudy"  : "D",
#         "rain"          : "i",
#         "chancesnow"    : "O",
#         "cloudy"        : "e",
#         "tstorms"       : "m",
#         "chancetstorms" : "K",
#         "sleet"         : "q",
#         "snow"          : "q",
#         "fog"           : "e",
#         "smoke"         : "e",
#         "haze"          : "e",
#         "flurries"      : "p",
#         "chanceflurries": "o",
#         "chancesleet"   : "o",
#         "clear"         : "A",
#         "partlysunny"   : "C",
#         }
#
#     try:
#         if (hour > 20 or hour < 6) and current is True:
#             new_icon = night_icon_dict[icon]
#         else:
#             new_icon = day_icon_dict[icon]
#     except KeyError:
#         print "Icon type doesn't exist. Please report this."
#         new_icon = ""
#
#     return new_icon