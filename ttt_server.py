import os
import ttt_game
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify, abort

app = Flask(__name__)

HOST = "/kayode-ezike-ttt.herokuapp.com"
PORT = 5000
VERIFICATION_TOKEN="OTibeqhO18dvugBdlI3eCNHx"

this_game = ttt_game.TTT_Game()

@app.route('/', methods=['POST'])
def basic_handler():
  token = request.form.get('token', None)
  command = request.form.get('command', None)
  command_input = request.form.get('text', None)

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
    if command_input == "display":
      return "Displaying Board...\n" + board.__str__()

  # Make a move
  elif command == "move":
    # verify proper input
    (fil, rnk) = cmd_input.split(' ')
    # Check if this valid file and rank
    # TODO
    if (0 <= board.file_to_rep(fil) < board.NUM_COLS) and (0 <= board.rank_to_rep(rnk) < board.NUM_ROWS):
      this_game.board.make_move(fil, rnk, 'x')

  else:
    return "Illegal command!"

  this_game.board.insert('a', 2, 'o')
  # return this_game.board.__str__()

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='', port=port)
