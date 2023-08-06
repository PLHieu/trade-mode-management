import copy
from datetime import datetime, date, timedelta
import pytz
import json

import urllib
from pymongo import MongoClient

if __name__ == "__main__":
    db_metatelebot = MongoClient("mongodb+srv://longhieu4820001:YI6YkQGnM3AGJgUH@cluster0.k0zyxgr.mongodb.net/?retryWrites=true&w=majority").get_database("metatelebot")
    col_trade_mode = db_metatelebot["trade_mode"]   

    current_time = datetime.now(tz=pytz.UTC) 
    print("check_and_reset_modes", current_time)

    list_item = list(col_trade_mode.find().limit(1000))
    for item in list_item:
        if item["expired_time"].replace(tzinfo=pytz.UTC) <= current_time:
            col_trade_mode.delete_one({"_id": item["_id"]})
    