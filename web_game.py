import bottle, sys
from bottlereact import BottleReact
import string
from bottle import request
import json
from bottle import HTTPResponse
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
  print(request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR'))
  return HTTPResponse(
          status=200,
          headers={
              "Content-Type": "application/json"
          },
          body=json.dumps({
                "gameState": ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
          })
      )

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