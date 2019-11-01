# You don't have to use these classes, but we recommend them as a good place to start!
import requests
from dotenv import load_dotenv
import os
import time
import datetime
import sqlite3
import pandas as pd
import pymongo

load_dotenv()

# # connect to database
# conn = sqlite3.connect('database.sqlite')
# cur = conn.cursor()

# # method to run SQL query
# def sql(query):
#     cur.execute(query)
#     df = pd.DataFrame(cur.fetchall())
#     df.columns = [x[0] for x in cur.description]
    # return df


class DataGetter():

  def __init__(self,database):
    conn = sqlite3.connect(database)
    self.CUR = conn.cursor()

  def sql(self,query):
    cur = self.CUR
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [x[0] for x in cur.description]
    return df



class WeatherGetter():

  def __init__(self):
    self.BASE_URL = 'https://api.darksky.net/forecast/'
    self.API_KEY = os.getenv("DARKSKY_API")

    if len(self.API_KEY) == 0:
      raise ValueError('Missing API key!')


  def getForcast(self, year, mth, day, lat = '52.52', long = '13.405'):
    exclude = 'exclude=daily,hourly,flags,alerts'
    d = datetime.date(year,mth,day)

    unixtime = int(float(time.mktime(d.timetuple())))
    url_option = "%s/%s,%s,%s?%s" %(self.API_KEY, lat, long, unixtime, exclude)
    url = self.BASE_URL + url_option

    response = requests.get(url)
    if response.status_code == 200:
      weather = response.json()

      if weather['currently'].get('icon'):
        condition = weather['currently'].get('icon')
      else:
        condition = weather['currently'].get('summary')

      print('Success')
    else:
      print('Error')
    return condition



class MongoHandler():

  def __init__(self):
    self.myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    self.mydb = self.myclient['matches_data']
    self.coll = self.mydb['team_stats']

  def getDataDict(self, name, tot_scores, tot_wins, win_perc_rain, graph = ''):
    team_data = {
                'name': name,
                'season': 2011,
                'total goals': tot_scores,
                'total wins': tot_wins,
                'rain day win %': win_perc_rain,
                'win_perc_graph': graph
                }
    return team_data

  def insertData(self, team_data):
    self.coll.insert_one(team_data)

