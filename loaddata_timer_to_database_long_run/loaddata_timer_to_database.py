from pymongo import MongoClient
from os import listdir
from os.path import join
from datetime import datetime
import json, requests
from secrets import getAppId
from time import sleep


client = MongoClient('localhost:27017')
weatherdb=client['Weather']
Historycollect = weatherdb['History']
Locationscollect = weatherdb['Locations']

data_dir = 'sampledata'

def insert_json_data(collect, city, data):
    insertNum = 0
    
    HourlyData = sorted(data['hourly'], key=lambda k: k['dt'])
    hourlydata_2 = []
    for counter, one in enumerate(HourlyData[:-1]):
        offset = HourlyData[counter+1]['dt'] - one['dt']
        if offset != 0:
            one['_id'] = one['dt']
            hourlydata_2.append(one)
    
    for hourly in hourlydata_2:
        exist = collect.count_documents({'dt': hourly['dt'],'location':city['location']})
        if(exist == 0):
            date = datetime.fromtimestamp(hourly['dt'])
            insertdata = {}
            insertdata['location'] = city['location']
            insertdata['year'] = date.year
            insertdata['month'] = date.month
            insertdata['day'] = date.day
            insertdata['hour'] = date.hour
            insertdata['dt'] = hourly['dt']
            insertdata['temp'] = hourly['temp']
            insertdata['feels_like'] = hourly['feels_like']
            insertdata['pressure'] = hourly['pressure']
            insertdata['humidity'] = hourly['humidity']
            insertdata['dew_point'] = hourly['dew_point']
            insertdata['clouds'] = hourly['clouds']
            insertdata['visibility'] = hourly['visibility'] if 'visibility' in hourly else -1
            insertdata['wind_speed'] = hourly['wind_speed']
            insertdata['wind_deg'] = hourly['wind_deg']
            insertdata['description_id'] = hourly['weather'][0]['id']
            collect.insert_one(insertdata)
            insertNum += 1
            
        elif(exist != 1):
            print('err!!', exist)
    return insertNum

def get_data_from_API(location):

    dt = datetime.now().timestamp() - 60*60*13 #offset for get 24 hr data

    out = requests.get('https://api.openweathermap.org/data/2.5/onecall/timemachine?lat='+location['lat']+'&lon='+location['lon']+'&dt='+dt+'&appid='+getAppId())
    return out.text

def timer():
    citylist = []
    try:
        result = Locationscollect.find()
        while True:
            onedata = result.next()
            citylist.append(onedata)
    except StopIteration:
        pass
    while True:
        for city in citylist:
            data = get_data_from_API(city)
            insertNum = insert_json_data(Historycollect, city, data)
            print(city['location'] + ' total insert num:', insertNum)
        sleep(12*60*60)