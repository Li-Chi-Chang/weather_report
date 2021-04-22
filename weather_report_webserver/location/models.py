from django.db import models

# Create your models here.

# get cities from db
from pymongo import MongoClient
Historycollect = MongoClient('localhost:27017')['Weather']['History']
locations = Historycollect.distinct('location')

