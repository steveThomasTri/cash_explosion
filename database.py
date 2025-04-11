import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
password = os.getenv("PASSWORD")
user = os.getenv("USER")

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  auth_plugin='caching_sha2_password',
  database='cedb'
  )

def insert_player(data):
  print(data)
  mycursor = mydb.cursor()

  if data["turn_4"][0] == "":
    data['turn_4'][0] = None
    data['turn_4'][1] = None
    data['turn_4'][2] = None

  sql = "INSERT INTO players (date,playerName,playerCity,ticketPurchasedStore,ticketPurchasedStreet, ticketPurchasedCity, number1,number1SpecialEvent, number1score, number2,number2SpecialEvent, number2score, number3,number3SpecialEvent, number3score, number4,number4SpecialEvent, number4score, bonus, gameTotal, isCashChallenge, isSecondChance, isChampion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

  datum = (data["date"],
           data["player_info"][0],
           data["player_info"][1],
           data["player_info"][2],
           data["player_info"][3],
           data["player_info"][4],
           data["turn_1"][0],
           data["turn_1"][1],
           data["turn_1"][2],
           data["turn_2"][0],
           data["turn_2"][1],
           data["turn_2"][2],
           data["turn_3"][0],
           data["turn_3"][1],
           data["turn_3"][2],
           data["turn_4"][0],
           data["turn_4"][1],
           data["turn_4"][2],
           data["bonus"],
           data["game_total"],
           False,
           False,
           False)
  
  mycursor.execute(sql, datum)

  mydb.commit()

def get_endgame(date):
  mycursor = mydb.cursor()
  sql = f"SELECT * FROM players where date= %s ORDER BY gameTotal DESC"
  addr = (date["date"],)
  mycursor.execute(sql, addr)
  myresult = mycursor.fetchall()
  return myresult