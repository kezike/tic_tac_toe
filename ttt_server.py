import os
import BaseHTTPServer
import ttt_game
from flask import Flask, request, jsonify, abort, current_app

app = Flask(__name__)

# HOST = "/kayode-ezike.chatly.io"
HOST = "/"
PORT = 5000
VERIFICATION_TOKEN = "OTibeqhO18dvugBdlI3eCNHx"

index_path = "/var/www/html/index.html"
this_game = ttt_game.TTT_Game()

# def do_display():

# def do_move():

@app.route(HOST, methods=['POST'])
def run_ttt():
  # Parse parameters
  token = request.form.get('token', None)
  command = request.form.get('command', None)
  cmd_input = request.form.get('text', None)

  print "command:", command

  # Validate parameters
  if not token or token != VERIFICATION_TOKEN:
    abort(400)
    return jsonify({
      "response_type": "ephemeral",
      "text": "Sorry, that didn't work. Please try again."
    })
  board = this_game.board
  # Confirm user's turn
  # TODO
  # Display board to user
  if command == "/ttt":
    print "Command is /ttt"
    print "TTT GAME"
    if text == "display":
      index = open(index_path, 'w')
      index.write(board.__str__())
      return board.__str__()

  # Make a move
  elif command == "move":
    # verify proper input
    (fil, rnk) = cmd_input.split(' ')
    # Check if this valid file and rank
    # TODO
    if (0 <= board.file_to_rep(fil) < board.NUM_COLS) and (0 <= board.rank_to_rep(rnk) < board.NUM_ROWS):
      this_game.board.make_move(fil, rnk, 'x')

'''
class TTT_Server(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self):
    # self.send_header("Content-type", "application/json")
    # self.send_header("Accept", "text/plain")
    # self.end_headers()
    self.wfile.write(ttt_game.TTT_Game().board.__str__())

def run_while_true(game, server_class=BaseHTTPServer.HTTPServer,
                   handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
  """
  This assumes that keep_running() is a function of no arguments which
  is tested initially and after each request.  If its return value
  is true, the server continues.
  """
  server_address = (HOST,PORT)
  httpd = server_class(server_address, handler_class)
  while not game.is_over():
    httpd.handle_request()

if __name__ == "__main__":
  print this_game.board
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((HOST, PORT), TTT_Server)
  print "Server Started At %s:%s" % (HOST, PORT)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print "Server Stopped At %s:%s" % (HOST, PORT)
'''

if __name__ == "__main__":
  port = int(os.environ.get("PORT", PORT))
  app.run(host='0.0.0.0', port=port)
