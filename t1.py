import schedule
import datetime


def kuku():
    h = datetime.datetime.now().hour % 12
    if h == 0:
        h = 12
    print('Ку' * h)


schedule.every().hour.at(':00').do(kuku)

while True:
    schedule.run_pending()