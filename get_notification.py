import requests

from model import col_notification
from datetime import datetime, date
import pytz

def get_notification():
    # skip vao t7, cn 
    today_week_day = date.today().weekday() 
    if today_week_day == 5 or today_week_day == 6:
        return 

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip",
        "appversion": "3.0",
        "cache-control": "no-cache",
        "connection": "Keep-Alive",
        "host": "18.142.141.159",
        "user-agent": "okhttp/4.9.2",
        "authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI5OTYzIiwiaWF0IjoxNjkxODM2NjQ3LCJleHAiOjE3MjMzNzI2NDd9.goStDlcPk7E6qUrup4xMLWfFaiTBVSEDtCVIUVQYf9WIxsPKl1ENddPjt1r_Ol552aEInJoLYudrzreA-7kLhg"
    }
    res = requests.get(f"http://18.142.141.159/api/notification", headers=headers)
    if res.status_code != 200:
        # TODO push to tele
        print(res.text)
        return 
    
    list_notis = res.json()

    # get latest id in db 
    last_noti = col_notification.find_one(sort=[('id', -1)])

    list_notis_gold = []
    # chi lay 100 noti dau tien trong list
    for noti in list_notis[:100]:
        # chi them nhung noti moi 
        if noti["id"] <= last_noti["id"]:
            break
        if "XAU" in noti["title"]:
            list_notis_gold.append(noti) 
    
    # bat dau goi api cho nhung noti nay
    list_notis_gold.reverse()
    for noti in list_notis_gold:
        # ghi vao db
        col_notification.insert_one(noti)

        res = requests.post(f"https://trade-signal-process.herokuapp.com/trade/ezsignal", data={
            "title": noti["title"],
            "text": noti["content"],
        })

        if res.status_code != 200:
            # TODO noti to tele
            print(res.text)
