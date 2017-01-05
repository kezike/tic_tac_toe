import os
import re
import ttt_game
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify, abort

app = Flask(__name__)

HOST = "/kayode-ezike-ttt.herokuapp.com"
PORT = 5000
VERIFICATION_TOKEN="OTibeqhO18dvugBdlI3eCNHx"

this_game = ttt_game.TTT_Game()

@app.route('/', methods=['POST'])
def ttt_handler():
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
    start_match = re.match("^start", command_input)
    start_match_flex = re.match("^start [1-26]$", command_input)
    display_match = re.match("^display$", command_input)
    move_match = re.match("^move [a-z] [1-26]$", command_input)
    help_match = re.match("^help$", command_input)
    if start_match:
      # TODO - Check if game already exists for channel
      # If not, set caller's piece to 'x',
      # set opponent's piece to 'o', and display board
      if start_match_flex:
        (start_cmd, dim) = command_input.split(' ')
        board.set_dim(dim)
      return board.__str__()
    elif display_match:
      return board.__str__()
    # This definition was placed here because we cannot access board.MAX_FILE until after "start" call
    move_match = re.match("^move [a-" + board.MAX_FILE + "] [1-" + str(board.NUM_ROWS) + "]$", command_input)
    # Make move
    elif move_match:
      # verify proper input
      print "COMMAND INPUT:", command_input
      (move_cmd, fil_str, rnk_str) = command_input.split(' ')
      rnk = int(rnk_str)
      print "fil:", fil_str
      print "rnk:", rnk
      # Check if this valid file and rank
      # TODO
      if (0 <= board.file_to_rep(fil_str) < board.NUM_COLS) and (0 <= board.rank_to_rep(rnk) < board.NUM_ROWS):
        this_game.make_move(fil_str, rnk, 'x')
        return board.__str__()
      else:
        return "Position (FILE, RANK) is out of bounds! Try again."
    elif help_match:
      manual = open("ttt_manual.txt", 'r')
      return manual.read()
    else:
      return "Illegal command! Type '/ttt help' for legal commands."
  return "OK"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='', port=port)
