from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from myfunctions import *

load_dotenv()


DATABASE = os.environ['DB_DATABASE']
HOST = os.environ['DB_HOST']
PASSWORD = os.environ['DB_PASSWORD']
USERNAME = os.environ['DB_USERNAME']

engine = create_engine("mysql+pymysql://"+USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE+"?charset=utf8mb4",
                      connect_args={
                        "ssl":{
                          "ssl_ca": "/etc/ssl/cert.pem"
                        }
                      })

def load_sessions_from_db():
  with engine.connect() as conn:
    statement = text("select * from ClassInformation")
    result = conn.execute(statement)
    result_dicts = []
    for row in result.all():
      row = row._asdict()
      start_time = row['ClassStartTime']
      end_time = row ['ClassEndTime']
      row['ClassStartTime'] = time_24_to_12(start_time)
      row['ClassEndTime'] = time_24_to_12(end_time)
      result_dicts.append(row)
    return result_dicts
