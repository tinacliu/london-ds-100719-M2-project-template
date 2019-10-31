# You don't have to use these classes, but we recommend them as a good place to start!
import requests
from dotenv import load_dotenv
import os
import time
import datetime
import sqlite3

load_dotenv()

class MongoHandler():
    pass

class WeatherGetter():

  def __init__(self):
    self.BASE_URL = 'https://api.darksky.net/forecast/'
    self.API_KEY = os.getenv("DARKSKY_API")

    if len(self.API_KEY) == 0:
      raise ValueError('Missing API key!')


  def getForcast(self, year, mth, day, lat = '52.52', long = '13.405'):
    exclude = 'exclude=currently,hourly,flags,alerts'
    d = datetime.date(year,mth,day)

    unixtime = int(float(time.mktime(d.timetuple())))
    url_option = "%s/%s,%s,%s?%s" %(self.API_KEY, lat, long, unixtime, exclude)
    url = self.BASE_URL + url_option

    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      print('Success')
    else:
      print('Error')
    return data



