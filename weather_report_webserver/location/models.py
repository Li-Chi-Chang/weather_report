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
    hightemp = collect.find_one({'location':location_name},sort=[('temp',-1)])
    lowtemp = collect.find_one({'location':location_name},sort=[('temp',1)])
    result['hightemp'] = hightemp['temp']
    result['lowtemp'] = lowtemp['temp']
    result['lowtemp_id'] = lowtemp['_id']
    result['hightemp_id'] = hightemp['_id']
    return result