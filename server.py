from flask import Flask, redirect, request
from json import dumps
from urllib.parse import urlencode
import requests,json
app = Flask(__name__)
app.debug = False
steam_openid_url = 'https://steamcommunity.com/openid/login'
json = {}

@app.route("/auth")
def auth_with_steam():

  params = {
    'openid.ns': "http://specs.openid.net/auth/2.0",
    'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.mode': 'checkid_setup',
    'openid.return_to': 'http://127.0.0.1:5000/authorize?season_id='+request.args.get("season_id"),
    'openid.realm': 'http://127.0.0.1:5000'
  }
  query_string = urlencode(params)
  auth_url = steam_openid_url + "?"+ query_string
  return redirect(auth_url)

@app.route("/authorize")
def authorize():
  print(request.args) 
  print(request.args.get("season_id")) 
  params = {'key': '2C7FF22BA6152ADD2C1A62E5760A8F75','format': 'json','steamids': request.args.get("openid.identity").split('/id/')[1]}
  response = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/',params=params).json()
  json[request.args.get("season_id")] = {"name" : response['response']['players'][0]['personaname'],"id":request.args.get("openid.identity").split('/id/')[1]} 
  return redirect("https://katocraftt.pages.dev/", code=302)

@app.route("/verify")
def verify():
  try:
      print(request.args.get("season_id"))
      if request.args.get("season_id") in json:
        return {'status' : True,'name':json[request.args.get("season_id")]['name']}
      return {'status' : False}
  except:
    return {'status' : False}
    
@app.route("/add")
def add():
  try:
      print(request.args.get("season_id"))
      if request.args.get("season_id") in json:
        return {'status' : True,'name':json[request.args.get("season_id")]['name']}
      return {'status' : False}
  except:
    return {'status' : False}
@app.route("/remove")
def remove():
  try:
      print(request.args.get("season_id"))
      if request.args.get("season_id") in json:
        return {'status' : True,'name':json[request.args.get("season_id")]['name']}
      return {'status' : False}
  except:
    return {'status' : False}

if __name__ == "__main__":
    app.run()


