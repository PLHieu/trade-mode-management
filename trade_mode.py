from model import col_trade_mode
from datetime import datetime, date, timedelta
import pytz

def delete_expired_trade_mode():
    # print("delete_expired_trade_mode")
    try:
        current_time = datetime.now(tz=pytz.UTC) 
        print("check_and_reset_modes", current_time)

        list_item = list(col_trade_mode.find().limit(1000))
        for item in list_item:
            if item["expired_time"].replace(tzinfo=pytz.UTC) <= current_time:
                col_trade_mode.delete_one({"_id": item["_id"]})
    except Exception as e:
        print(str(e))