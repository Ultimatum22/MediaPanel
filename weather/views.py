import json
import os
import re
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
    forecast_astronomy_url = base_url + "/astronomy/q/%s.json" % quote(location)
    forecast_10_days_url = base_url + "/conditions/forecast10day/q/%s.json" % quote(location)
    forecast_current_url = base_url + "/conditions/q/%s.json" % quote(location)
    # forecast_hourly_url = base_url + "/hourly/q/%s.json" % quote(location)

    print "Fetching forecast for 10 days... ", forecast_10_days_url

    try:
        forecast_astronomy_response = urlopen(forecast_astronomy_url)
        forecast_10_days_response = urlopen(forecast_10_days_url)
        forecast_current_response = urlopen(forecast_current_url)
        # forecast_hourly_response = urlopen(forecast_hourly_url)
    except URLError as e:
        if hasattr(e, 'reason'):
            print e.reason
        elif hasattr(e, 'code'):
            print "Status returned: " + str(e.code)

    astronomy_data = json.loads(forecast_astronomy_response.read().decode())
    ten_days_forecast_data = json.loads(forecast_10_days_response.read().decode())
    current_forecast_data = json.loads(forecast_current_response.read().decode())
    # hourly_forecast_data = json.loads(forecast_hourly_response.read().decode())

    print 'astronomy_data: ', astronomy_data
    print 'current_forecast_data: ', current_forecast_data

    try:
        current_forecast = current_forecast_data['current_observation']
        ten_days_forecast = ten_days_forecast_data['forecast']['simpleforecast']['forecastday']
    except KeyError:
        print 'No Data'

    print "Data fetched successfully"

    pattern = re.compile(r'[A-Za-z]+ \d+ (.+):(.+):\d+')
    time_string = current_forecast['local_time_rfc822']
    hour = int(pattern.search(time_string).group(1))
    minute = int(pattern.search(time_string).group(2))

    weather_icon = current_forecast['icon']
    if hour >= astronomy_data['sun_phase']['sunset']['hour'] and minute > astronomy_data['sun_phase']['sunset']['minute']:
        print 'Sunset - night'
        weather_icon_css = "wi-night-" + weather_icon
    else:
        print 'Sunrise - day'
        if weather_icon == 'clear':
            weather_icon = 'sunny'
        weather_icon_css = "wi-day-" + weather_icon

    weather_html = '<table style="width: 100%; border-top: 1px solid rgba(255,255,255,.1);"><tbody><tr>'
    weather_html += '<td style="padding: 0 20px 15px 20px; width: 250px;">'
    weather_html += '<div class="bright large">' + str(current_forecast['temp_c']) + '<sup>&deg;</sup>'
    weather_html += '<span class="wi ' + weather_icon_css + '" style="font-size: 70px;" title="clear"></span>'
    weather_html += '</div>'

    weather_html += '<div class="semi-bold">'

    wind = "%s kph %s" % (current_forecast['wind_kph'], current_forecast['wind_dir'])

    weather_html += '<span class="wi wi-strong-wind"></span> ' + wind + ' &nbsp;&nbsp;'

    # TODO, make function
    if hour >= astronomy_data['sun_phase']['sunset']['hour'] and minute > astronomy_data['sun_phase']['sunset']['minute']:
        print 'Sunset'
        weather_html += '<span class="wi wi-sunrise"></span> %s:%s</div>' % (astronomy_data['sun_phase']['sunrise']['hour'], astronomy_data['sun_phase']['sunrise']['minute'])
    else:
        print 'Sunrise'
        weather_html += '<span class="wi wi-sunset"></span> %s:%s</div>' % (astronomy_data['sun_phase']['sunset']['hour'], astronomy_data['sun_phase']['sunset']['minute'])

    weather_html += '</td>'

    # count = 1

    # forecast_iter = enumerate(forecast)
    # forecast_iter.next();
    # for i, node in forecast_iter:
    for node in ten_days_forecast[:6]:
        date = node['date']

        print 'Node: ', node

        weather_icon = node['icon']
        if hour >= astronomy_data['sun_phase']['sunset']['hour'] and minute > astronomy_data['sun_phase']['sunset']['minute']:
            print 'Sunset - night'
            weather_icon_css = "wi-night-" + weather_icon
        else:
            print 'Sunrise - day'
            if weather_icon == 'clear':
                weather_icon = 'sunny'
            elif weather_icon == 'partlycloudy':
                weather_icon = 'sunny-overcast'

            weather_icon_css = "wi-day-" + weather_icon

        weather_html += '<td style="padding: 5px 40px; text-align: center; border-left: 1px solid rgba(255,255,255,.1); line-height: 2em;">'
        weather_html += '<div class="day bold" style="margin-bottom: 15px">' + date['weekday'] + '</div>'
        weather_html += '<span class="wi ' + weather_icon_css + ' bright medium"></span><br/>'
        weather_html += '<span class="bright semi-bold" style="margin: 0 10px;">' + node['high']['celsius'] + '</span>'
        weather_html += '<span class="bright semi-bold" style="margin: 0 10px;">' + node['low']['celsius'] + '</span></td>'

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