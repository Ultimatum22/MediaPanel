import json
import os
import re
from urllib2 import URLError, urlopen
from mediapanel.settings import BASE_DIR

__author__ = 'Dave'


class WeatherSettings(object):
    settings = None
    file_path = None

    def __init__(self):
        if not WeatherSettings.settings:
            WeatherSettings.file_path = os.path.join(BASE_DIR, 'weather', ".pywu.conf")

            with open(WeatherSettings.file_path) as config:
                WeatherSettings.settings = json.load(config)

    def __getattr__(self, item):
        return WeatherSettings.settings[item]


class WeatherPath():
    now = "conditions"
    forecast10day = "forecast10day"
    hourly = "hourly"
    astronomy = "astronomy"

    def __init__(self, type):
        self.value = type

    def __eq__(self, other):
        return self.value == other.value


class WeatherUnderground(object):

    settings = WeatherSettings()
    current_forecast = None
    hourly = None
    astronomy_data = None
    forecast = None

    def make_api_url(self, path):
        base_url = "http://api.wunderground.com/api/%s/" % self.settings.api_key
        location = "/q/%s.json" % self.settings.location

        return base_url + path + location

    def get_weather_data(self, path):

        print 'url: ', self.make_api_url(path)
        try:
            response = urlopen(self.make_api_url(path))
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'Error reason: ' + e.reason
            elif hasattr(e, 'code'):
                print 'Error code:' + str(e.code)

        data = json.loads(response.read().decode())

        if 'error' in data['response']:
            print data['response']['error']['description']
            return

        if 'results' in data['response']:
            print 'More than 1 city matched your query, try being more specific'
            for result in data['response']['results']:
                print '%s, %s %s' % (result['name'], result['state'], result['country_name'])
            return

        if path == WeatherPath.now:
            self.current_forecast = data['current_observation']
        elif path == WeatherPath.hourly:
            self.hourly = data['hourly_forecast']
        elif path == WeatherPath.astronomy:
            self.astronomy_data = data
        elif path == WeatherPath.forecast10day:
            self.forecast = data['forecast']['simpleforecast']['forecastday']

    def get_sun_phase(self, local_time):
        # astronomy_data = self.get_weather_data(WeatherPath.astronomy)

        pattern = re.compile(r'[A-Za-z]+ \d+ (.+):(.+):\d+')
        hour = int(pattern.search(local_time).group(1))
        minute = int(pattern.search(local_time).group(2))

        if hour >= self.astronomy_data['sun_phase']['sunset']['hour'] and (hour >= self.astronomy_data['sun_phase']['sunset']['hour'] or minute > self.astronomy_data['sun_phase']['sunset']['minute']):
            return 'sunset'
        else:
            return 'sunrise'

    def get_weather_icon(self, icon, local_time=None):
        if local_time is not None and self.get_sun_phase(local_time) == 'sunset':
            return 'wi-night-' + icon
        else:
            if icon == 'clear':
                icon = 'sunny'
            elif icon == 'partlycloudy':
                icon = 'sunny-overcast'
            elif icon == 'chancerain':
                icon = 'rain'
            return 'wi-day-' + icon