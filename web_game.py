import bottle, sys
from bottlereact import BottleReact
import string
from bottle import request
import json

'''
Game Logic 
'''
class UrGame():
  def __init__(self, key):
    self.GAME_KEY = key
    self.boardState = [] 

'''
Run Server  
'''

PROD = '--prod' in sys.argv

app = bottle.Bottle()
#br = BottleReact(app, prod=PROD, render_server=False)
br = BottleReact(app, prod=PROD, verbose=True)

@app.get('/Game')
def root():
  return br.render_html(
    br.Game({})
  )

@app.post('/hiddenRequest')
def test():
  data_bytes = request._get_body_string()
  print(json.loads(data_bytes))

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