from django.shortcuts import render

# Create your views here.
def main(request):
    from django.shortcuts import render
    from . import models

    locationsinfo = []
    
    for location in models.get_locations():
        onedata = {}
        onedata['name'] = location
        onedata['link'] = location
        locationsinfo.append(onedata)

    return render(request, 'main.html', {
        'locations': locationsinfo,
    })

def location(request):
    from django.shortcuts import render
    from . import models, secrets
    import requests,json
    from datetime import datetime
    from django.http import HttpResponseNotFound

    city = request.path[1:]
    cityinfo = models.get_city_info(city)
    if cityinfo is None:
        return HttpResponseNotFound('hello')

    current_weather = json.loads(requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+str(cityinfo['lat'])+'&lon='+str(cityinfo['lon'])+'&appid='+secrets.getAppId()).text)
    time = current_weather['dt'] + current_weather['timezone']
    date = datetime.utcfromtimestamp(time)

    history_info = models.get_history_info(city)
    return render(request, 'location.html', {
        'location': current_weather['name'],
        'date': str(date.date()),
        'time': str(date.time()),
        'temp_in_K': round(current_weather['main']['temp'],2),
        'temp_in_C': round(current_weather['main']['temp'] - 273.15,2),
        'temp_in_F': round((current_weather['main']['temp']*1.8) - 459.67,2),
        'feels_like_in_K': round(current_weather['main']['feels_like'],2),
        'feels_like_in_C': round(current_weather['main']['feels_like'] - 273.15,2),
        'feels_like_in_F': round((current_weather['main']['feels_like']*1.8) - 459.67,2),
        'humidity': current_weather['main']['humidity'],
        'wind_speed': current_weather['wind']['speed'],

        'history_date_from': history_info['history_from'],
        'history_date_to': history_info['history_to'],

        'htemp_in_K': round(history_info['hightemp'],2),
        'htemp_in_C': round(history_info['hightemp'] - 273.15,2),
        'htemp_in_F': round((history_info['hightemp']*1.8) - 459.67,2),
        'ltemp_in_K': round(history_info['lowtemp'],2),
        'ltemp_in_C': round(history_info['lowtemp'] - 273.15,2),
        'ltemp_in_F': round((history_info['lowtemp']*1.8) - 459.67,2),

        'avgtemp_in_K': round(history_info['avgtemp'],2),
        'avgtemp_in_C': round(history_info['avgtemp'] - 273.15,2),
        'avgtemp_in_F': round((history_info['avgtemp']*1.8) - 459.67,2),

        'ltemp_id':history_info['lowtemp_id'],
        'htemp_id':history_info['hightemp_id'],
    })

def history(request):
    from django.shortcuts import render
    from . import models

    obj_id = request.path.split('/')[-1]
    record = models.get_one_record(obj_id)

    return render(request, 'history.html', {
        'location': record['location'],
        'year': record['year'],
        'month': record['month'],
        'day': record['day'],
        'hour': record['hour'],
        'temp_in_K': round(record['temp'],2),
        'temp_in_C': round(record['temp'] - 273.15,2),
        'temp_in_F': round((record['temp']*1.8) - 459.67,2),
        'feels_like_in_K': round(record['feels_like'],2),
        'feels_like_in_C': round(record['feels_like'] - 273.15,2),
        'feels_like_in_F': round((record['feels_like']*1.8) - 459.67,2),
        'pressure': record['pressure'],
        'dew_point': record['dew_point'],
        'humidity': record['humidity'],
        'wind_speed': record['wind_speed'],
        'description_main': record['description_main'],
        'description_detail': record['description_detail'],
    })

def search(request):
    from django.shortcuts import render
    from . import models
    descriptions = models.get_description_list()
    locations = [{'name':'empty', 'value':''}]
    for location in models.get_locations():
        locations.append({'name':location, 'value':location})
    return render(request, 'search.html',{
        'location_list': locations,
        'description_main_list': descriptions,
    })

def search_post(request):
    from django.shortcuts import render
    from . import models
    result = models.get_query_from_data(dict(request.POST))
    return render(request, 'searchback.html',{
        'records':result['records'],

    })