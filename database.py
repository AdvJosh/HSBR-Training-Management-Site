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


def load_single_session_from_db(ClassID):
  with engine.connect() as conn:
    statement = text("SELECT * FROM ClassInformation WHERE ClassID = :ClassID")
    values = {'ClassID' : ClassID}
    result = conn.execute(statement, values)
    result_dict = []
    result = result.fetchone()
    result_dict = result._asdict()
    result_dict['ClassDate'] = convert_jd_to_date(result_dict['ClassDate'])
    start_time = result_dict['ClassStartTime']
    end_time = result_dict['ClassEndTime']
    result_dict['ClassStartTime'] = time_24_to_12(start_time)
    result_dict['ClassEndTime'] = time_24_to_12(end_time)
    return result_dict


def load_sessions_for_one_person(EmpID):
  with engine.connect() as conn:
    statement = text("SELECT * FROM ClassRoster WHERE EmpID = :EmpID")
    values = {'EmpID' : EmpID}
    roster_result = conn.execute(statement, values)
    roster_result_list = []
    result_dict = []
    for row in roster_result.all():
      row = row._asdict()
      roster_result_list.append(row['ClassID'])
  class_information = load_sessions_from_db()
  for row in class_information:
    if row['ClassID'] in roster_result_list:
      result_dict.append(row)
  return result_dict