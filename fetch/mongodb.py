# -*- coding: utf-8 -*-
import json
from fetch.setting import *
import pymongo

__author__ = 'Administrator'


class DataBase():
    def __init__(self):
        self.server = MONGODB_SERVER
        self.port = MONGODB_PORT
        self.db = MONGODB_DB
        self.col = MONGODB_COLLECTION
        connection = pymongo.Connection(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]
    def update(self,entity):
      self.collection.save(json.loads(json.dumps(entity, default=lambda o: o.__dict__)))

    def find(self,id):
        return self.collection.find_one({"_id":id})

    def filterNoResult(self):
        return self.collection.find({"teamPairs":{"$elemMatch":{"vsResult":""}}})

dataBase=DataBase()



