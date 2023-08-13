import schedule
import time


from get_notification import get_notification
from trade_mode import delete_expired_trade_mode
from get_signal import get_new_signals

schedule.every(5).to(8).seconds.do(get_new_signals)
schedule.every(10).minutes.do(delete_expired_trade_mode)

while True:
    schedule.run_pending()
    time.sleep(1)