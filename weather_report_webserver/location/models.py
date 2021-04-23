from django.db import models
from bson.objectid import ObjectId

# Create your models here.

# get cities from db
from pymongo import MongoClient
def get_locations():
    collect = MongoClient('localhost:27017')['Weather']['History']
    locations = collect.distinct('location')
    return locations
# get location lat lon
def get_city_info(location_name):
    collect = MongoClient('localhost:27017')['Weather']['Locations']
    return collect.find_one({'location':location_name})

def get_one_record(obj_id):
    collect = MongoClient('localhost:27017')['Weather']['History']
    record = collect.find_one({'_id':ObjectId(obj_id)})
    collect = MongoClient('localhost:27017')['Weather']['Description']
    description = collect.find_one({'_id':record['description_id']})
    record['description_main'] = description['main']
    record['description_detail'] = description['description']
    return record

def get_history_info(location_name):
    result = {}
    collect = MongoClient('localhost:27017')['Weather']['History']
    history_from = collect.find_one({'location':location_name},sort=[('dt',1)])
    history_to = collect.find_one({'location':location_name},sort=[('dt',-1)])

    hightemp = collect.find_one({'location':location_name},sort=[('temp',-1)])
    lowtemp = collect.find_one({'location':location_name},sort=[('temp',1)])
    avgtemp = collect.aggregate([
        {'$match':{'location':location_name}},
        {'$group': {'_id':'$location', 'temp': {'$avg':'$temp'}}}
    ]).next()

    result['history_from'] = str(history_from['month']) + '/' + str(history_from['day']) + '/' + str(history_from['year'])
    result['history_to'] = str(history_to['month']) + '/' + str(history_to['day']) + '/' + str(history_to['year'])
    result['hightemp'] = hightemp['temp']
    result['lowtemp'] = lowtemp['temp']
    result['avgtemp'] = avgtemp['temp']
    result['lowtemp_id'] = lowtemp['_id']
    result['hightemp_id'] = hightemp['_id']
    return result

def get_description_list():
    collect = MongoClient('localhost:27017')['Weather']['Description']
    description_main_list = ['empty']
    description_main_list.extend(collect.distinct('main'))
    description_detail_list = []
    for main in description_main_list:
        description_detail_list.append({'name':main})
        description_detail_list[-1]['list'] = []
    description_detail_list[0]['list'].append({'id':0, 'description':'empty'})

    listcursor = collect.find(sort=[('_id',1)])
    try:
        while True:
            onedata = listcursor.next()
            for one in description_detail_list:
                if (one['name'] == onedata['main']):
                    one['list'].append({'id':onedata['_id'], 'description':onedata['description']})
    except StopIteration:
        pass
    return description_detail_list