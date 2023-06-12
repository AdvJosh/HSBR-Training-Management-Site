from sqlalchemy import create_engine, text
import os


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
    result = conn.execute(text("select * from ClassInformation"))
  
    result_dicts = []
    for row in result.all():
      result_dicts.append(row._asdict())
    print(result_dicts)
    return result_dicts

load_sessions_from_db()