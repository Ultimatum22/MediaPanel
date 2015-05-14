from django.http import HttpResponse

# temp_file = os.path.join('MediaPanel', 'tmp', 'pywu.cache.json')
# conf_file = os.path.join(BASE_DIR, 'weather', ".pywu.conf")
from weather.weather_underground import WeatherUnderground, WeatherPath

weather = WeatherUnderground()

def index(request):
    pass


def forecast(request):
    weather.get_weather_data(WeatherPath.astronomy)
    weather.get_weather_data(WeatherPath.now)
    weather.get_weather_data(WeatherPath.forecast10day)

    # if weather.get_sun_phase(current_forecast['local_time_rfc822']):

    weather_html = '<table style="width: 100%; border-top: 1px solid rgba(255,255,255,.1);"><tbody><tr>'
    weather_html += '<td style="padding: 0 20px 15px 20px; width: 250px;">'
    weather_html += '<div class="bright large">' + str(weather.current_forecast['temp_c']) + '<sup>&deg;</sup>'
    weather_html += '<span class="wi ' + weather.get_weather_icon(weather.current_forecast['icon'], weather.current_forecast['local_time_rfc822']) + '" style="font-size: 70px;" title="clear"></span>'
    weather_html += '</div>'

    wind = "%s kph %s" % (weather.current_forecast['wind_kph'], weather.current_forecast['wind_dir'])

    weather_html += '<div class="semi-bold">'
    weather_html += '<span class="wi wi-strong-wind"></span> ' + wind + ' &nbsp;&nbsp;'

    if weather.get_sun_phase(weather.current_forecast['local_time_rfc822']) == 'sunset':
        weather_html += '<span class="wi wi-sunrise"></span> %s:%s</div>' % (weather.astronomy_data['sun_phase']['sunrise']['hour'], weather.astronomy_data['sun_phase']['sunrise']['minute'])
    else:
        weather_html += '<span class="wi wi-sunset"></span> %s:%s</div>' % (weather.astronomy_data['sun_phase']['sunset']['hour'], weather.astronomy_data['sun_phase']['sunset']['minute'])

    weather_html += '</td>'

    for node in weather.forecast[:4]:
        date = node['date']

        weather_html += '<td style="padding: 5px 40px; text-align: center; border-left: 1px solid rgba(255,255,255,.1); line-height: 2em;">'
        weather_html += '<div class="day bold medium">' + date['weekday'] + '</div>'
        weather_html += '<span class="wi ' + weather.get_weather_icon(node['icon']) + ' bright medium" style="margin: 10px 0"></span><br/>'
        weather_html += '<span class="bright semi-bold medium" style="margin: 0 10px;">' + node['high']['celsius'] + '</span>'
        weather_html += '<span class="bright semi-bold medium" style="margin: 0 10px;">' + node['low']['celsius'] + '</span></td>'

    weather_html += '</tr></tbody></table>'

    return HttpResponse(weather_html)