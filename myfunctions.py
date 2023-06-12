"""
This is a parking spot for various functions to keep the app.py file cleaner
"""
import os
from datetime import datetime
import pytz

def get_current_cst_time():
  utcmoment = datetime.utcnow()
  localFormat = "%A, %b %-d, %-y | %I:%M %p"
  localDatetime = utcmoment.astimezone(pytz.timezone('America/Chicago'))
  localDatetime = localDatetime.strftime(localFormat)
  return localDatetime