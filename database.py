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

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM players")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
