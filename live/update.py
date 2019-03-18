
import os
import sys
import math
import os.path
import pickle
import json
import cv2
from pymongo import MongoClient
import datetime


mod_cf = 'names.cf'
test_client = MongoClient()
test_db = test_client['test_db']
test_col = test_db['test_col']

def init_db_entry(name):
    # initiate
    json_obj = {}
    json_obj['_id'] = str(name)
    json_obj['freq'] = 1
    json_obj['time'] = datetime.datetime.now()
    test_col.insert_one(json_obj)

prev_update = []

while True:
    update = {}
    with open(mod_cf, 'r') as f:
        update = json.load(f)
    print(update)

    for entry in update:
        if entry not in prev_update and update[entry] > 25:
            prev_update.append(entry)
            #############################################
            ####
            #############################################
            result_freq = test_col.update({'_id': entry}, {'$inc': {'freq': 1}})
            result_datetime = test_col.update({'_id': entry}, {'$set': {'time': datetime.datetime.now()}})

            cursor = test_col.find({})
            for document in cursor:
                    print(document)


    #init_db_entry('Unknown'+str(unknown_count))


    # cursor = test_col.find({})
    # for document in cursor:
    #         print(document)

