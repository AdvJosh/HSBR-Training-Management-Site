from sqlalchemy import create_engine, text, insert
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

def verify_login_from_db(login_dict):
  with engine.connect() as conn:
    statement = text("SELECT * FROM EmployeeData WHERE EmpID = :EmpID AND EmpDoB LIKE '%:BirthYear'")
    result = conn.execute(statement, login_dict)
    result = result.fetchone()
    if result == None:
      result = {}
      result['valid'] = False
      return result
    else:
      result = result._asdict()
      result['valid'] = True
      return result


def check_sign_in_status(ClassID,EmpID):
  with engine.connect() as conn:
    statement = text("SELECT * FROM ClassSignin WHERE EmpID = :EmpID AND ClassID = :ClassID")
    values = {}
    values['EmpID'] = EmpID
    values['ClassID'] = ClassID
    result = conn.execute(statement, values)
    result = result.fetchone()
    if result == None:
      return None
    else: 
      return True
    


def session_sign_in_to_db(session_signin_dict):
  session_data = {}
  with engine.connect() as conn:
    statement = text("Select * FROM ClassInformation WHERE SessionCode=:SessionCode")
    result = conn.execute(statement, session_signin_dict)
    result =  result.fetchone()
    if result == None:
      result = {}
      result['debug'] = 'Couldnt find class'
      result['valid'] = False
      return result
    else:
      session_data = result._asdict()
  with engine.connect() as conn:
    statement = text("SELECT * FROM ClassSignin WHERE EmpID = :EmpID and SessionCode = :SessionCode")
    result = conn.execute(statement, session_signin_dict)
    result = result.fetchone()
    if result != None:
      result = {}
      result['debug'] = 'Duplicate'
      result['valid'] = False
      return result
  # Lets construct the dict of data for the db
  db_insert_dict = {}
  db_insert_dict['ClassID'] = session_data['ClassID']
  db_insert_dict['EmpID'] = session_signin_dict['EmpID']
  db_insert_dict['SessionCode'] = session_signin_dict['SessionCode']
  db_insert_dict['TimeCST'] = get_current_cst_time_db()
  db_insert_dict['ClassDate'] = get_current_jd_date()
  with engine.connect() as conn:
    statement = text("INSERT INTO ClassSignin (ClassID, EmpID, SessionCode, TimeCST, ClassDate) VALUES (:ClassID, :EmpID, :SessionCode, :TimeCST, :ClassDate)")
    result = conn.execute(statement, db_insert_dict)
    conn.commit()
  result = {}
  result['ClassName'] = session_data['ClassName']
  result['valid'] = True
  return result


def emp_db_lookup(emp_lookup_dict):
  with engine.connect() as conn:
    # Fix the statement parsing for this, it is not good from a security standpoint
    statement = "SELECT * FROM EmployeeData WHERE EmpName Like '%"\
    + str(emp_lookup_dict['EmpName']) + "%'"
    statement = text(statement)
    result = conn.execute(statement)
    result_dict = []
    for row in result.all():
      row = row._asdict()
      date = convert_dob_jd_to_date(row['EmpDoB'])
      row['EmpDoB'] = date
      result_dict.append(row)
    return result_dict