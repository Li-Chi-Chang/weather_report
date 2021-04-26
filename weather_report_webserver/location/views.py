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

        'avgtemp_in_Spring': history_info['avgtemp_in_Spring'],
        'avgtemp_in_Summer': history_info['avgtemp_in_Summer'],
        'avgtemp_in_Fall': history_info['avgtemp_in_Fall'],
        'avgtemp_in_Winter': history_info['avgtemp_in_Winter'],
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

        'htemp_in_K':round(result['temp'][0]['temp'],2),
        'htemp_in_C':round(result['temp'][0]['temp'] - 273.15,2),
        'htemp_in_F':round((result['temp'][0]['temp']*1.8) - 459.67,2),
        'htemp_id':result['temp'][0]['_id'],

        'ltemp_in_K':round(result['temp'][1]['temp'],2),
        'ltemp_in_C':round(result['temp'][1]['temp'] - 273.15,2),
        'ltemp_in_F':round((result['temp'][1]['temp']*1.8) - 459.67,2),
        'ltemp_id':result['temp'][1]['_id'],

        'avgtemp_in_K': round(result['avg']['temp'],2),
        'avgtemp_in_C': round(result['avg']['temp'] - 273.15,2),
        'avgtemp_in_F': round((result['avg']['temp']*1.8) - 459.67,2),

        'hftemp_in_K':round(result['feels_like'][0]['temp'],2),
        'hftemp_in_C':round(result['feels_like'][0]['temp'] - 273.15,2),
        'hftemp_in_F':round((result['feels_like'][0]['temp']*1.8) - 459.67,2),
        'hftemp_id':result['feels_like'][0]['_id'],

        'lftemp_in_K':round(result['feels_like'][1]['temp'],2),
        'lftemp_in_C':round(result['feels_like'][1]['temp'] - 273.15,2),
        'lftemp_in_F':round((result['feels_like'][1]['temp']*1.8) - 459.67,2),
        'lftemp_id':result['feels_like'][1]['_id'],

        'avgftemp_in_K': round(result['avg']['feels_like'],2),
        'avgftemp_in_C': round(result['avg']['feels_like'] - 273.15,2),
        'avgftemp_in_F': round((result['avg']['feels_like']*1.8) - 459.67,2),
    })