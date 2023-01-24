# %%
import os
from os.path import join, dirname
# %%
import psycopg2
from dotenv import load_dotenv

# %%
def connect_db(ap='heroku'): #or local
  load_dotenv(verbose=True)
  if(ap == 'heroku'):
    print("Heroku PostgreSQL!")
    dotenv_path = join(dirname(__file__), './env/.env_heroku')
    load_dotenv(dotenv_path)
  elif(ap == 'local'):
    print("Local PostgreSQL!")
    dotenv_path = join(dirname(__file__), './env/.env_local')
    load_dotenv(dotenv_path)

  DATABASE = os.environ.get("DATABASE")
  USER = os.environ.get("USER")
  PASSWORD = os.environ.get("PASSWORD")
  HOST = os.environ.get("HOST")
  PORT = os.environ.get("PORT")

  connection = psycopg2.connect(
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
    )
  return connection


#%%
def disconect_db():
  cursor.close()
  connection.close()
  print("Disconectted PostgreSQL!")
#%%
connection = connect_db()
cursor = connection.cursor()
disconect_db()
#INSERT INTO SEND_HIS(WM_DATE, WM_NAME, SEND_STATUS, CREATE_DATE) VALUES (TO_TIMESTAMP('2021/03/09 09:00:00','YY-MM-DD HH24:MI:SS'),null,null,null);
#%%
def insert_wmdate(wmdate):
  #wmdate::str  '2021/03/09 09:00:00'
  sql = "INSERT INTO SEND_HIS(WM_DATE, WM_NAME, SEND_STATUS, CREATE_DATE,UPDATE_DATE) VALUES (TO_TIMESTAMP('{0}','YY-MM-DD HH24:MI:SS'),null,null,sysdate,sysdate)'".format(wmdate)
  cursor.execute(sql)
#%%
def update_wmname(wmdate, wmname):
  sql = "UPDATE SEND_HIS SET WM_NAME = {0}, UPDATE = sysdate WHERE WM_DATE = {2}".format(wmname, wmdate)
  cursor.execute(sql)
#%%
def update_status(wmname):
  sql = "UPDATE SEND_HIS SET SEND_STATUS = 1, UPDATE = sysdate WHERE WM_NAME = {0}".format(wmname)
  cursor.execute(sql)
#%%
def check_db(wmdate):
  sql = "SELECT * FROM SEND_HIS WHERE CREATE_DATE >= TO_TIMESTAMP('{0}','YY-MM-DD HH24:MI:SS') ORDER BY CREATE_DATE DESC LIMIT 20".format(wmdate)
  cursor.execute(sql)
#%%
def read_db():
  results = cursor.fetchall()
  for row in results:
    print((row[0]).strftime('%Y/%m/%d %H:%M:%S'))
#%%
