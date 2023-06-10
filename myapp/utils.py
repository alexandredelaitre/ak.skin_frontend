import json
from urllib.parse import urlparse

import pyotp
from myapp import db
from .models import Item
import requests



def get_steam_id(url):
  parsed_url = urlparse(url)
  steam_id = parsed_url.path.split('/')[-1]
  return steam_id

def get_steam_profile(steam_id, api_key):
  url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'
  response = requests.get(url)
  data = response.json()['response']['players'][0]
  return data

def parseInventory(steam64):
  #use steamwebapi instead
  
  #open intentory.json
  json_data = json.load(open('myapp/inventory.json'))
  

  print(json_data['assets'])
  #print(json_data)
  inventory = []
  try:
    assets = json_data['assets']
    descriptions = json_data['descriptions']
    
    for i in range(len(assets)):
      asset=assets[i]
      description = descriptions[i]
      
      #print(description['market_name'],description['name'], description['icon_url'], description['descriptions'], description['tradable'], description['name_color'],description['commodity'],description['type'],description['marketable'],description['tags'], description['market_tradable_restriction'])
      inventoryObject = {
        'assetid': asset['assetid'],
        'market_name': description['market_name'],
        'market_hash_name': description['market_hash_name'],
        'name': description['name'],
        'icon_url': description['icon_url'],
        'descriptions': description['descriptions'],
        'tradable': description['tradable'],
        'name_color': description['name_color'],
        'commodity': description['commodity'],
        'type': description['type'],
        'marketable': description['marketable'],
        'tags': description['tags'],
        'market_tradable_restriction': description['market_tradable_restriction'],
        'number_owned': asset['amount'],
        'tradable': description['tradable'],
      }
      if i==0:
        print(inventoryObject)
      #print("\n")
      if asset['appid']==730:
        if inventoryObject['tradable']==1:
          #price = requests.get("https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name="+inventoryObject['market_hash_name']).json()
          try:
            #if float(price['lowest_price'].replace("$",""))>0.04:
              if "Sealed Graffiti" not in description['market_name']:
                inventory.append(inventoryObject)
                #Check if item is in database, if not add it
                #print(inventoryObject['market_hash_name'])
                #print(inventoryObject)
                if Item.query.filter_by(market_hash_name=inventoryObject['market_hash_name']).first() is None:
                  """class Item(db.Model):
                    id = db.Column(db.Integer, primary_key=True)
                    market_name = db.Column(db.String(80), unique=True, nullable=False)
                    market_hash_name = db.Column(db.String(80), unique=True, nullable=False)
                    name = db.Column(db.String(80), nullable=False)
                    icon_url = db.Column(db.String(80), nullable=False)
                    descriptions = db.Column(db.String(80), nullable=False)
                    tradable = db.Column(db.String(80), nullable=False)
                    name_color = db.Column(db.String(80), nullable=False)
                    commodity = db.Column(db.String(80), nullable=False)
                    type = db.Column(db.String(80), nullable=False)
                    marketable = db.Column(db.String(80), nullable=False)
                    tags = db.Column(db.String(80), nullable=False)
                    itemid = db.Column(db.String(80), nullable=False)
                    """
                  newItem = Item(name=inventoryObject['name'],
                                  market_name=inventoryObject['market_name'], 
                                  market_hash_name=inventoryObject['market_hash_name'], 
                                  icon_url=inventoryObject['icon_url'], 
                                  descriptions=inventoryObject['descriptions'], 
                                  tradable=inventoryObject['tradable'], 
                                  name_color=inventoryObject['name_color'], 
                                  commodity=inventoryObject['commodity'], 
                                  type=inventoryObject['type'], 
                                  marketable=inventoryObject['marketable'],
                                  tags=inventoryObject['tags'], 
                                  itemid=inventoryObject['assetid'])
                  db.session.add(newItem)
                  db.session.commit()
                  print("added item to database")
                

          except Exception as e:
            #print(e)
            print(inventoryObject['market_hash_name']+" is not tradable")
  except Exception as e:
    pass
  return inventory


