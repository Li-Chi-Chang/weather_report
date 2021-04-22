from pymongo import MongoClient
from os import listdir
from os.path import join
from datetime import datetime
import json

citylist = ['FortWayne','Taipei']

client = MongoClient('localhost:27017')
weatherdb=client['Weather']
Historycollect = weatherdb['History']

def insert_json_data(collect, cityname):
    insertNum = 0
    for one_file in listdir('data'):
        HourlyData = []
        if(cityname in one_file):
            location = json.loads(open(join('data',one_file)).read())['hourly']
            for hourly in location:
                HourlyData.append(hourly)
    
        HourlyData = sorted(HourlyData, key=lambda k: k['dt'])
        hourlydata_2 = []
        for counter, one in enumerate(HourlyData[:-1]):
            offset = HourlyData[counter+1]['dt'] - one['dt']
            if offset != 0:
                one['_id'] = one['dt']
                hourlydata_2.append(one)

        
        for hourly in hourlydata_2:
            exist = collect.count_documents({'dt': hourly['dt'],'location':cityname})
            if(exist == 0):
                date = datetime.fromtimestamp(hourly['dt'])
                insertdata = {}
                insertdata['location'] = cityname
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

# mian
for city in citylist:
    insertNum = insert_json_data(Historycollect, city)
    print(city + ' total insert num:', insertNum)