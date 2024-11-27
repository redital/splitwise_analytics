import mysql.connector
from mysql.connector import errorcode

from config import database_config

def initialize():
  try:
      mydb = mysql.connector.connect(**database_config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)

    return mydb

def ricerca_entity_non_caricate(mydb,df):
  mydb = mysql.connector.connect(**database_config)
  mydb.connect()
  if mydb and mydb.is_connected():
      with mydb.cursor() as cursor:

          query = cursor.execute("SELECT Id FROM prova")

          rows = cursor.fetchall()

          ids = [row[0] for row in rows]
          result = df[~df["Id"].isin(ids)]

      mydb.close()
      return result

  else:
      print("Could not connect")
      return


def update_db(mydb,diff):
  mydb = mysql.connector.connect(**database_config)
  if mydb and mydb.is_connected():
      with mydb.cursor() as cursor:
        sql =  "INSERT INTO `prova` (`Id`, `Description`, `Date`, `Category`, `Details`, `Cost`, `Currency`, `Created by`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        
        for i in list(range(len(diff)-1,-1,-1)):
          val = (
                  int(diff['Id'][i]), 
                  diff['Description'][i], 
                  diff['Date'][i], 
                  diff['Category'][i], 
                  diff['Details'][i], 
                  diff['Cost'][i], 
                  diff['Currency'][i], 
                  diff['Created by'][i]
          )
          cursor.execute(sql, val)

        mydb.commit()

      mydb.close()
      return 0

  else:
      print("Could not connect")
      return None





