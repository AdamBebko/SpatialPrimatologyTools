import datetime

def toDatetime(text):
    date = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    return date