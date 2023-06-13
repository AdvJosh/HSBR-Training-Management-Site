"""
This is a parking spot for various functions to keep the app.py file cleaner
"""
import os
from datetime import datetime, timedelta
import pytz

def get_current_cst_time():
  utcmoment = datetime.utcnow()
  localFormat = "%A, %b %-d, %-y | %I:%M %p"
  localDatetime = utcmoment.astimezone(pytz.timezone('America/Chicago'))
  localDatetime = localDatetime.strftime(localFormat)
  return localDatetime

def get_current_jd_date():
  utcmoment = datetime.utcnow()
  localFormat = "%-j%Y"
  localDatetime = utcmoment.astimezone(pytz.timezone('America/Chicago'))
  localDatetime = localDatetime.strftime(localFormat)
  return localDatetime


def get_current_cst_time_db():
  utcmoment = datetime.utcnow()
  localFormat = "%I%M"
  localDatetime = utcmoment.astimezone(pytz.timezone('America/Chicago'))
  localDatetime = localDatetime.strftime(localFormat)
  return localDatetime

def time_24_to_12(time_to_convert):
    if len(str(time_to_convert)) < 4:
        time_to_convert = '0' + str(time_to_convert)
    time = datetime.strptime(str(time_to_convert), "%H%M")
    return time.strftime("%-I:%M %p")

def convert_jd_to_date(jd):
    date_format = '%A, %B %-d, %Y'
    day = int(str(jd)[:-4])
    year = int(str(jd)[-4:])
    start_date = datetime(year, 1, 1)
    # add the number of days to the start date
    result_date = start_date + timedelta(days=day-1)
    # format the date string using the specified format
    return result_date.strftime(date_format)