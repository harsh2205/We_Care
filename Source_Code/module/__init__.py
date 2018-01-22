from datetime import datetime, timedelta


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current.time()
        current += delta


dts = [dt.strftime("%I:%M %p") for dt in
       datetime_range(datetime(2016, 9, 1, 7), datetime(2016, 9, 1, 9+12),
       timedelta(minutes=30))]

print(dts)


time4 = ''