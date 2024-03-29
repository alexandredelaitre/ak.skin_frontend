import hashlib
import hmac
import math
import os
import secrets
import threading
import time
from urllib.parse import urlencode
from flask import Blueprint, Response, session, jsonify
from myapp import db
from myapp.models import User, UserSpecificItems
from .utils import parseInventory
from flask import render_template, redirect, request, url_for
import requests
from openid.consumer import consumer
import urllib
from flask_login import login_required, login_user, logout_user, current_user

from flask_socketio import SocketIO, emit
from . import socketio
from steampy.client import SteamClient, Asset
from steampy.utils import GameOptions
#
import uuid
import os
print(os.getcwd())


main = Blueprint('main', __name__)
STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"



@main.route('/protected')
@login_required
def protected_route():
    # Only authenticated users can access this route
    return "You are logged in!"

@socketio.on('trade_url')
def trade_url(data):
    print(data)
    user = User.query.filter_by(steamid=current_user.steamid).first()
    user.tradeurl = data
    db.session.commit()
    emit('trade_url', data, broadcast=False)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/settings")
def settings():
    return render_template("settings.html")

@main.route("/make_trade_offer", methods=['POST'])
def make_trade_offer():
    
    data = request.json  # Assuming the arrays are sent as JSON in the request body

    move_to_akskins = data['move_to_akskins']
    move_to_steam = data['move_to_steam']
    print(move_to_akskins)
    print(move_to_steam)
    
    
    """
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
      }"""


    url = 'https://steamcommunity.com/tradeoffer/new/?partner=151014203&token=GCsZHrSq'
    
    
    

    payload = {
        'move_to_akskins': move_to_akskins,
        'move_to_steam': move_to_steam,
        'url': url,
        'code': uuid.uuid4().hex[:6]
    }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_token'
}
    test = requests.post('',json=payload, headers=headers)
    print(test)

        


    

    return 'Array processed successfully'


@main.route("/offer_accepted", methods=['POST'])
def offer_accepted():
    data = request.json
    print(data)

    return 'Array processed successfully'

@main.route("/login_dummy")
def steam_login_return():
    if True:
        steam_id="1"
        user = User.query.filter_by(steamid=steam_id).first()
        if user is None:
            user = User(steamid=steam_id, balance=0.0, tradeurl="", email="", name="", avatar="https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTVvKAffVNh8bcKrd7o8w_WGTNv6K_Wxhd8qgZGfNfTw7z1WcHrrfKXrzujGvr16BaTRQ2tYbPxFwnHtlA")
            db.session.add(user)
            db.session.commit()
            print("User added to database")
        else:
            user.avatar = "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTVvKAffVNh8bcKrd7o8w_WGTNv6K_Wxhd8qgZGfNfTw7z1WcHrrfKXrzujGvr16BaTRQ2tYbPxFwnHtlA"
            db.session.commit()
        login_user(user)
        return redirect(url_for('main.profile'))
    else:
        return "Failed to log in with Steam"

@main.route("/item/<item>", methods=['GET'])
def item(item):
    item = []
    return render_template("item.html", item=item)


@main.route("/profile")
def profile():
    
    steam_id = current_user.steamid
    # Do something with the steam_id
    return render_template("profile.html", steam_id=steam_id)
    

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route("/exchange")
def exchange():
    return render_template("exchange.html")

@main.route("/buy")
def buy():
    return render_template("buy.html")

@main.route("/sell")
def sell():
    return render_template("sell.html")

@main.route('/itemset/<itemset>', methods=['GET'])
def itemsets(itemset):
    print(itemset.lower())
    if itemset.lower() in ['knives','shotguns','pistols','smgs','rifles','snipers','contraband']:
        print("yo")
        items = UserSpecificItems.query.filter_by(type=itemset).all()
        items = [item.serialize() for item in items]
        return jsonify(items)

@main.route('/inventory')
def inventory():
    #steamid = current_user.steamid
    inventory_data = parseInventory("76561198111279931")

    return render_template("inventory.html", inventory=inventory_data, akskin_inventory=[])

@main.route("/authorize")
def authorize():
    # Get the user's Steam ID
    steam_id = request.args.get("openid.claimed_id").split("/")[-1]
    
    # Get the user's profile information
    profile_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api_key}&steamids={steam_id}"
    profile_response = requests.get(profile_url)
    profile_data = profile_response.json()
    print(profile_data)
    # Get the user's inventory
    print("HELLOOOOOO")
    inventory_data = parseInventory(steam_id)
    #print(inventory_data)
    
    # Extract the user's username and profile picture URL from the profile data
    username = profile_data["response"]["players"][0]["personaname"]
    profile_picture_url = profile_data["response"]["players"][0]["avatarmedium"]
    
    #log the user in
    print(steam_id, type(steam_id))
    

    # Render a template with the user's username, profile picture, and inventory data
    return render_template("authorized.html", username=username, profile_picture_url=profile_picture_url, inventory=inventory_data)
