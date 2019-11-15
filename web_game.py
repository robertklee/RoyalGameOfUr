import bottle, sys
from bottlereact import BottleReact
import string
from bottle import request
import json
from bottle import HTTPResponse
from datetime import datetime, timedelta

from game_logic import Game

'''
Run Server  
'''

PROD = '--prod' in sys.argv

app = bottle.Bottle()
#br = BottleReact(app, prod=PROD, render_server=False)
br = BottleReact(app, prod=PROD, verbose=True)

games = {} 
previousCheck = datetime.today()
checkDelta = timedelta(0, 20, 0)

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

  if (datetime.today() - previousCheck > checkDelta):
    gameManager()
    previousCheck = datetime.today()

  if request_data['game_key'] not in games.keys():
    games[request_data['game_key']] = Game(cookie)
    returnVal = games[request_data['game_key']].handleClick(cookie, request_data['clickPosition'])
  else:
    returnVal = games[request_data['game_key']].handleClick(cookie, request_data['clickPosition'])
  return HTTPResponse(
          status=200,
          headers={
              "Content-Type": "application/json",
              # "Access-Control-Allow-Origin": "*",
          },
          body=json.dumps(returnVal)
      )

def gameManager():
  for k, v in games.items():
    delta = datetime.today() - v.mostRecentValidClick
    if delta > Game.timeDeltaForSuspension:
      v.suspended = True
  
  if (len(games) > Game.maxActiveGames):
    for k, v in games.items():
      if v.suspended:
        del games[k]
      
      if (len(games) <= Game.maxActiveGames):
        break

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

def run():
  bottle.debug(not PROD)
  bottle.run(
    app=app, 
    host='localhost',
    port='2081',
    reloader=not PROD
  )

if __name__=='__main__':
  run()