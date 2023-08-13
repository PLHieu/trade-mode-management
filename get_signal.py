import requests

from model import col_notification, col_signals
from datetime import datetime, date, timezone, timedelta
import pytz

def get_new_signals():
    # print("get_new_signals")
    try:
        # skip khung thoi gian vao ban dem  
        current_time = datetime.now(tz=pytz.timezone("Asia/Saigon"))
        # tuong duong voi 23h dem, va 4 gio sang vnt
        if current_time.hour >= 0 and current_time.hour <= 3:
            return 

        # skip vao t7, cn 
        today_week_day = current_time.weekday()
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
        res = requests.get(f"http://18.142.141.159/api/signals", headers=headers)
        if res.status_code != 200:
            # TODO push to tele
            print(res.text)
            return 
        
        data = res.json()

        for day_str, signals in data["content"].items():
            for s in signals:
                if "XAU" not in s["pairs"]:
                    continue

                # check trong db xem thu da co signal nay chua
                item = col_signals.find_one({"id": s["id"]})
                if item != None:
                    continue
                
                # goi request 
                signal_text = f"{day_str}\n{s['type']} XAUUSD\nENTRY {s['openPrice']}\n✅TP1: {s['tp1']}\n✅TP2: {s['tp2']}\n✅TP3: {s['tp3']}\n❌SL:  {s['stopLoss']}" 
                res = requests.post(f"https://trade-signal-process.herokuapp.com/trade/create", json={
                    "signal": signal_text,
                    "account_name": "real_en_zero_1",
                    "source": "ezsignal_group_tele",
                })

                if res.status_code != 200:
                    # TODO noti to tele
                    print(res.text)

                # insert vao db
                col_signals.insert_one(s)
    
    except Exception as err:
        print(str(err))