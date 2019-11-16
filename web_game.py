import bottle, sys
from bottlereact import BottleReact
import string
from bottle import request
import json
from bottle import HTTPResponse
import threading
import time
import sqlite3

from game_logic import Game

'''
Run Server  
'''

PROD = '--prod' in sys.argv

app = bottle.Bottle()
#br = BottleReact(app, prod=PROD, render_server=False)
br = BottleReact(app, prod=PROD, verbose=True)

# Active Game Dict
games = {} 
# Database
conn = sqlite3.connect("Logs") # TODO finish and figure out
curs = conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS Game_Server_Connection_Logs (cookie STRING PRIMARY KEY, accesses INT);")


@app.get('/Game')
def root():
  return br.render_html(
    br.Game({})
  )

@app.put('/hiddenRequest')
def test():
  data_bytes = request._get_body_string()

  request_data = json.loads(data_bytes)
  cookie = request_data['cookie']
  returnVal = None
  # Handle new clients 
  print(request_data)
  curs.execute("SELECT COUNT(*) FROM Game_Server_Connection_Logs WHERE cookie=\"" + str(cookie).replace("-","") + "\";")
  if curs.fetchone()[0] > 0:
    curs.execute("INSERT INTO Game_Server_Connection_Logs (cookie, accesses) VALUES (\"" + str(cookie).replace("-","") + "\", 1);")
  else:
    curs.execute("UPDATE Game_Server_Connection_Logs SET accesses = accesses + 1 WHERE cookie = \"" + str(cookie).replace("-","") + "\";")
    

  if request_data['game_key'] not in games.keys():  
    games[request_data['game_key']] = [Game(cookie), 100]
    returnVal = games[request_data['game_key']][0].handleClick(cookie, request_data['clickPosition'])
  else:
    returnVal = games[request_data['game_key']][0].handleClick(cookie, request_data['clickPosition'])
    games[request_data['game_key']][1] = 100
  return HTTPResponse(
          status=200,
          headers={
              "Content-Type": "application/json",
              # "Access-Control-Allow-Origin": "*",
          },
          body=json.dumps(returnVal)
      )

# @bottle.route('/<:re:.*>', method='OPTIONS')
# def enable_cors_generic_route():
#     """
#     This route takes priority over all others. So any request with an OPTIONS
#     method will be handled by this function.

#     See: https://github.com/bottlepy/bottle/issues/402

#     NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
#     """
#     add_cors_headers()

# @bottle.hook('after_request')
# def enable_cors_after_request_hook():
#     """
#     This executes after every route. We use it to attach CORS headers when
#     applicable.
#     """
#     add_cors_headers()

# def add_cors_headers():
#     if True:  # You don't have to gate this
#         bottle.response.headers['Access-Control-Allow-Origin'] = '*'
#         bottle.response.headers['Access-Control-Allow-Methods'] = \
#             'GET, POST, PUT, OPTIONS'
#         bottle.response.headers['Access-Control-Allow-Headers'] = \
#             'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


def TTL():
  while (True):
    for game_key in games.keys():
      games[game_key][1] -= 1
      if games[game_key][1] <= 0:
        games.popitem(game_key)
    time.sleep(6)
    

def run():
  x = threading.Thread(target=TTL, args=())
  x.start()
  bottle.debug(not PROD)
  bottle.run(
    app=app, 
    host='localhost',
    port='2081',
    reloader=not PROD
  )

if __name__=='__main__':
  run()