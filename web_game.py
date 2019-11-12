import bottle, sys
from bottlereact import BottleReact
import string
from bottle import request
import json
from bottle import HTTPResponse

from bottle import request, Bottle, abort
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

@app.put('/hiddenRequest')
def test():
  data_bytes = request._get_body_string()
  print(json.loads(data_bytes))
  print(request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR'))
  return HTTPResponse(
          status=200,
          headers={
              "Content-Type": "application/json",
              # "Access-Control-Allow-Origin": "*",
          },
          body=json.dumps({
                "gameState": ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
          })
      )


# @app.route('/websocket')
# def handle_websocket():
#     wsock = request.environ.get('wsgi.websocket')
#     if not wsock:
#         abort(400, 'Expected WebSocket request.')

#     while True:
#         try:
#             message = wsock.receive()
#             wsock.send("Your message was: %r" % message)
#         except WebSocketError:
#             break

# from gevent.pywsgi import WSGIServer
# from geventwebsocket import WebSocketError
# from geventwebsocket.handler import WebSocketHandler
# server = WSGIServer(("0.0.0.0", 8080), app,
#                     handler_class=WebSocketHandler)
# server.serve_forever()

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