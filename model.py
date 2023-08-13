import urllib
from pymongo import MongoClient

db_metatelebot = MongoClient("mongodb+srv://longhieu4820001:YI6YkQGnM3AGJgUH@cluster0.k0zyxgr.mongodb.net/?retryWrites=true&w=majority").get_database("metatelebot")
col_trade_mode = db_metatelebot["trade_mode"]   
col_notification = db_metatelebot["notification"]
col_signals = db_metatelebot["ez_signal"] 