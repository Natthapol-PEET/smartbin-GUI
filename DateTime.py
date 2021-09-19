import datetime

def get_date():
    date_object = datetime.datetime.now()
    date = date_object.strftime('%d/%m/%Y')
    return str(date)

def get_time():
    time_object = datetime.datetime.now()
    time = time_object.strftime('%H:%M')
    return str(time)

def create_timeout():
    return datetime.timedelta(hours=0, minutes=14, seconds=30)

def get_start_time():
    return datetime.datetime.now()

def get_end_time():
    return datetime.datetime.now()

def calculate_time(start, timeout):
    result = get_end_time() - start
    time = timeout - result
    time_split = str(time).split(':')
    minute = str(time_split[1])
    seconds = str(time_split[2].split('.')[0])

    time_str = minute + ':' + seconds
    return str(time_str)
