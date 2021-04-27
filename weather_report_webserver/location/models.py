from django.db import models
from bson.objectid import ObjectId
from datetime import datetime

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
    spring = None
    try:
        spring = collect.aggregate([
            {'$match':{'location':location_name, 'month':{'$gte':3,'$lte':5}}},
            {'$group': {'_id':'', 'temp': {'$avg':'$temp'}}}
        ]).next()['temp']
    except:
        pass
    summer = None
    try:
        summer = collect.aggregate([
            {'$match':{'location':location_name, 'month':{'$gte':6,'$lte':8}}},
            {'$group': {'_id':'', 'temp': {'$avg':'$temp'}}}
        ]).next()['temp']
    except:
        pass
    fall = None
    try:
        fall = collect.aggregate([
            {'$match':{'location':location_name, 'month':{'$gte':9,'$lte':11}}},
            {'$group': {'_id':'', 'temp': {'$avg':'$temp'}}}
        ]).next()['temp']
    except:
        pass
    winter = None
    try:
        spring = collect.aggregate([
            {'$match':{'location':location_name, 'month':{'$or':[{'$gte':12}, {'$lte':2}]}}},
            {'$group': {'_id':'', 'temp': {'$avg':'$temp'}}}
        ]).next()['temp']
    except:
        pass

    result['avgtemp_in_Spring'] = round((spring*1.8) - 459.67,2) if spring is not None else 'no data'
    result['avgtemp_in_Summer'] = round((summer*1.8) - 459.67,2) if summer is not None else 'no data'
    result['avgtemp_in_Fall'] = round((fall*1.8) - 459.67,2) if fall is not None else 'no data'
    result['avgtemp_in_Winter'] = round((winter*1.8) - 459.67,2) if winter is not None else 'no data'
    return result

def get_description_list():
    collect = MongoClient('localhost:27017')['Weather']['Description']
    description_main_list = ['empty']
    description_main_list.extend(collect.distinct('main'))
    description_detail_list = []
    for main in description_main_list:
        description_detail_list.append({'name':main})
        description_detail_list[-1]['list'] = []
    description_detail_list[0]['list'].append({'id':'', 'description':'empty'})

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

def get_query_from_data_helper_onedata_from_to(query, from_info,to_info, query_column, mytype):
    if from_info != '' or to_info != '':
        query[query_column] = {}
        if from_info != '':
            query[query_column]['$gte'] = mytype(from_info)
        if to_info != '':
            query[query_column]['$lte'] = mytype(to_info)

def get_query_from_data_helper_dt_function(date_in):
    return int(datetime.timestamp(datetime.strptime(date_in,'%Y-%m-%dT%H:%M')))

def get_query_from_data(post_data):
    query = {}
    if post_data['query_location'][0] != '':
        query['location'] = post_data['query_location'][0]
    get_query_from_data_helper_onedata_from_to(query,post_data['query_time_from'][0],post_data['query_time_to'][0],'dt',get_query_from_data_helper_dt_function)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_temp_from'][0],post_data['query_temp_to'][0],'temp',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_feellike_from'][0],post_data['query_feellike_to'][0],'feels_like',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_pressure_from'][0],post_data['query_pressure_to'][0],'pressure',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_humidity_from'][0],post_data['query_humidity_to'][0],'humidity',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_dew_point_from'][0],post_data['query_dew_point_to'][0],'dew_point',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_wind_speed_from'][0],post_data['query_wind_speed_to'][0],'wind_speed',int)
    get_query_from_data_helper_onedata_from_to(query,post_data['query_description_detail'][0],post_data['query_description_detail'][0],'description_id',int)
    collect = MongoClient('localhost:27017')['Weather']['History']
    results = collect.find(query,{'location':1, 'month':1, 'day':1, 'year':1, 'hour':1},sort=[('location',1),('dt',1)])
    result_links = []
    try:
        while True:
            onedata = results.next()
            result_links.append({'link':'/history/' + str(onedata['_id']),'name':onedata['location'] + ' ' + str(onedata['month']) + '/' + str(onedata['day']) + '/' + str(onedata['year']) + ' ' + str(onedata['hour']) + ':00'})
    except StopIteration:
        pass
    highrealtemp = collect.find_one(query,{'temp':1},sort=[('temp',-1)])
    lowrealtemp = collect.find_one(query,{'temp':1},sort=[('temp',1)])
    highfeeltemp = collect.find_one(query,{'feels_like':1},sort=[('feels_like',-1)])
    lowfeeltemp = collect.find_one(query,{'feels_like':1},sort=[('feels_like',1)])
    avg = {'temp': 0, 'feels_like':0}
    try:
        avg = collect.aggregate([
            {'$match':query},
            {'$group': {'_id':'', 'temp': {'$avg':'$temp'}, 'feels_like': {'$avg':'$feels_like'}}}
        ]).next()
    except StopIteration:
        pass
    
    return {'records_num':len(result_links),'records':result_links,'temp':[highrealtemp,lowrealtemp],'feels_like':[highfeeltemp,lowfeeltemp], 'avg':avg}
    