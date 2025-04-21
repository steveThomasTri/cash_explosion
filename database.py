import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#using a connection pool
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
  sql = f"SELECT * FROM players where date= %s ORDER BY gameTotal DESC, playerName DESC"
  #Must resolve for tie breaker
  addr = (date["date"],)
  mycursor.execute(sql, addr)
  myresult = mycursor.fetchall()
  return myresult

def update_endgame_results(result):
  values_list = result["isCashChallenge"]  # example list of players
  placeholders = ','.join(['%s'] * len(values_list))

  sql = f"UPDATE players SET isCashChallenge = 1 WHERE date = %s AND playerName IN ({placeholders})"
  params = [result["date"]] + values_list

  mycursor = mydb.cursor()
  mycursor.execute(sql, params)
  mydb.commit()

  mycursor = mydb.cursor()
  sql = f"UPDATE players SET isSecondChance = 1 where date= %s AND playerName=%s"
  addr = (result["date"],result["isSecondChance"],)
  mycursor.execute(sql, addr)
  mydb.commit()

  #champion
  #if new champ, new row goes in champions table
  #if returning, get id and copy to champions table with new date
  if result["isChampion"] != "":
    sql = f"UPDATE players SET isChampion = 1 where date= %s AND playerName=%s"
    addr = (result["date"],result["isChampion"],)
    mycursor.execute(sql, addr)
    mydb.commit()

    sql = """
    INSERT INTO champions (date, playerID)
    VALUES (
      %s,
      (SELECT id FROM players WHERE date= %s AND playerName=%s)
    )
    """

    params = (result["date"], result["date"], result["isChampion"],)
    mycursor.execute(sql, params)
    mydb.commit()
  else:
    sql = """
    INSERT INTO champions (date, playerID)
    SELECT %s, t.playerID FROM (
      SELECT playerID FROM champions ORDER BY id DESC LIMIT 1
    ) AS t
    """
    params = (result["date"],)
    mycursor.execute(sql, params)
    mydb.commit()

def verify2(date):
  mycursor = mydb.cursor()
  sql = f"SELECT * FROM players where date= %s AND isCashChallenge = 1"
  addr = (date["date"],)
  mycursor.execute(sql, addr)
  myresult = mycursor.fetchall()
  cashchallenge = len(myresult)
  sql = f"SELECT * FROM players where date= %s AND isSecondChance = 1"
  addr = (date["date"],)
  mycursor.execute(sql, addr)
  myresult = mycursor.fetchall()
  secondchance = len(myresult)
  return cashchallenge, secondchance

def totalwinnings(date):
  mycursor = mydb.cursor()
  sql = f"SELECT isChampion, isSecondChance FROM players where date= %s AND isChampion = 1"
  addr = (date["date"],)
  mycursor.execute(sql, addr)
  myresult = mycursor.fetchone()
  #results will be (1,0) (1,1) or None
  #if returning champioon wins
  if myresult == None:
    print("OK")
    mycursor = mydb.cursor()
    sql = """
    SELECT
    (select sum(bonus) from players where date= %s group by date) +
    (select sum(gameTotal) from players where date= %s group by date) +
    (select sum(gameTotal) from players where date= %s AND isCashChallenge = 1 group by date) +
    (5000) +
    (SELECT 
      CASE 
        WHEN cnt = 2 THEN 50000
        WHEN cnt > 2 THEN 100000
        ELSE 0
      END
    FROM (
      SELECT COUNT(*) AS cnt
      FROM champions
      WHERE playerID = (
        SELECT playerID FROM champions ORDER BY id DESC LIMIT 1
      )
    ) AS total_sum)
    """
    addr = (date["date"],date["date"],date["date"],)
    mycursor.execute(sql, addr)
    myresults = mycursor.fetchone()
    return myresults
  elif myresult[0] == 1 and myresult[1] == 0:
    mycursor = mydb.cursor()
    sql = """
    SELECT
    (select sum(bonus) from players where date= %s group by date) +
    (select sum(gameTotal) from players where date= %s group by date) +
    (select sum(gameTotal) from players where date= %s AND isCashChallenge = 1 group by date) +
    (5000) +
    (select sum(
      CASE
        when gameTotal + gameTotal >= 40000 THEN 75000 - gameTotal - gameTotal
        else 50000 - gameTotal - gameTotal
      END) 
    FROM players WHERE date= %s AND isChampion = 1) AS total_sum
    """
    addr = (date["date"],date["date"],date["date"],date["date"],)
    mycursor.execute(sql, addr)
    myresults = mycursor.fetchone()
    return myresults
  elif myresult[0] == 1 and myresult[1] == 1:
    mycursor = mydb.cursor()
    sql = """
    -- Case when the Second Chance player is the champion
    SELECT
    -- all players bonus totals
    (select sum(bonus) from players where date= %s group by date) +
    -- all players game totals
    (select sum(gameTotal) from players where date= %s group by date) +
    -- the two players with cash challenge
    (select sum(gameTotal) from players where date= %s AND isCashChallenge = 1 group by date) +
    -- including second chance
    (5000) +
    (select sum(
    CASE
      when gameTotal + gameTotal >= 40000 THEN 75000 - gameTotal - gameTotal
        -- always happens
        else 50000 - gameTotal - 5000
    END) from players WHERE date= %s AND isChampion = 1 and isSecondChance = 1) AS total_sum
    """
    addr = (date["date"],date["date"],date["date"],date["date"],)
    mycursor.execute(sql, addr)
    myresults = mycursor.fetchone()
    return myresults

def cities():
  mycursor = mydb.cursor()
  sql = """
  SELECT city, lon, lat, county, count(ticketPurchasedCity), 
  sum(
  CASE
    when (isCashChallenge = 1 and isChampion = 0) then gameTotal + gameTotal
      when (isSecondChance = 1 and isChampion = 0) then gameTotal + 5000
      when (isChampion = 1) then 
      CASE
        when coalesce(champ_count.champion_count, 0) = 2 then 100000
              when champ_count.champion_count = 1 then 50000
          END
      else gameTotal
  END) as GT
  from cities 
  INNER JOIN players 
  ON cities.city = players.ticketPurchasedCity
  LEFT JOIN 
      (
          SELECT playerID, COUNT(*) AS champion_count
          FROM champions
          GROUP BY playerID
      ) AS champ_count ON champ_count.playerID = players.id
  GROUP BY cities.city, cities.lon, cities.lat, cities.county ORDER BY GT desc;  
"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def county():
  mycursor = mydb.cursor()
  '''
  #Data is based on the ticket Purchased city
  sql = "select count(ticketPurchasedCity) AS contestantCount, floor(avg(code)), county, round(avg(gameTotal),2) from players inner join cities on players.ticketPurchasedCity = cities.city group by county"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  #print(myresult)
  countyData = {}
  for result in myresult:
    #print(result)
    countyData[str(result[1])] = {"ticketpurchasedcount":result[0],"averagebase":result[3], "name":result[2]}
  return countyData
  '''
  sql = '''
  SELECT
    tp.county AS county,
    COALESCE(tp.countyCode, hc.countyCode) AS countyCode,
    tp.ticketPurchasedCount,
    tp.ticketPurchasedTotal,
    hc.homeCountyCount,
    hc.homeCountyTotal
  FROM (
    SELECT
      county,
      FLOOR(AVG(code)) AS countyCode,
      COUNT(ticketPurchasedCity) AS ticketPurchasedCount,
      ROUND(AVG(gameTotal), 2) AS ticketPurchasedTotal
    FROM players
    INNER JOIN cities ON players.ticketPurchasedCity = cities.city
    GROUP BY county
  ) tp
  LEFT JOIN (
    SELECT
      county,
      FLOOR(AVG(code)) AS countyCode,
      COUNT(playerCity) AS homeCountyCount,
      ROUND(AVG(gameTotal), 2) AS homeCountyTotal
    FROM players
    INNER JOIN cities ON players.playerCity = cities.city
    GROUP BY county
  ) hc ON tp.county = hc.county

  UNION

  -- RIGHT JOIN part: home county data with no matching ticket purchase data
  SELECT
    hc.county AS county,
    COALESCE(tp.countyCode, hc.countyCode) AS countyCode,
    tp.ticketPurchasedCount,
    tp.ticketPurchasedTotal,
    hc.homeCountyCount,
    hc.homeCountyTotal
  FROM (
    SELECT
      county,
      FLOOR(AVG(code)) AS countyCode,
      COUNT(ticketPurchasedCity) AS ticketPurchasedCount,
      ROUND(AVG(gameTotal), 2) AS ticketPurchasedTotal
    FROM players
    INNER JOIN cities ON players.ticketPurchasedCity = cities.city
    GROUP BY county
  ) tp
  RIGHT JOIN (
    SELECT
      county,
      FLOOR(AVG(code)) AS countyCode,
      COUNT(playerCity) AS homeCountyCount,
      ROUND(AVG(gameTotal), 2) AS homeCountyTotal
    FROM players
    INNER JOIN cities ON players.playerCity = cities.city
    GROUP BY county
  ) hc ON tp.county = hc.county
  WHERE tp.county IS NULL;
  '''
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  countyData = {}
  for result in myresult:
    countyData[str(result[1])] = {"ticketpurchasedcount":result[2],"ticketpurchasedbase":result[3], "homecountytotal":result[4], "homecountybase":result[5], "name":result[0]}
  return countyData

def weekdata():
  mycursor = mydb.cursor()
  sql = """
  select date, 
  sum(bonus) + 
  sum(
    (case
      when isChampion = 1 then (
        case
          when gameTotal + gameTotal >= 40000 then 75000
                  else 50000
              end
              )
      when (isChampion = 0 and isSecondChance = 1) then gameTotal + 5000
          when (isChampion = 0 and isCashChallenge = 1) then gameTotal + gameTotal
      else gameTotal
    end)
  ) +
  (
  case
    when sum(isChampion) = 0 then 50000
    else 0
  end
  ) as GT
  from players group by date;  
"""
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  weekData = []
  for result in myresult:
    #print(result)
    weekData.append({"date":result[0],"value":result[1]})
  return weekData

def numbers():
  mycursor = mydb.cursor()
  sql = """
  SELECT
    number,
    COUNT(*) AS total_count,
    COUNT(CASE WHEN specialEvent != '' THEN 1 END) AS special_event_count,
    round(AVG(score),2) AS avg_score
  FROM number_view
  GROUP BY number
  ORDER BY number;  
  """
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  numberData = []
  for result in myresult:
    #print(result)
    numberData.append({"number":result[0],"count":result[1],"specialeventcount":result[2],"avgscore":result[3]})
  return numberData
