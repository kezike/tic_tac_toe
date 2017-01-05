import os
import re
import ttt_game
import ttt_rep
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
    display_match = re.match("^display$", command_input)
    move_match = re.match("^move [a-z] ([1-9] | [1-2][0-6])$", command_input)
    help_match = re.match("^help$", command_input)
    if start_match:
      # TODO - Check if game already exists for channel
      # If not, set caller's piece to 'x',
      # set opponent's piece to 'o', and display board
      
      # Configure dimensions of board
      start_match_flex = re.match("^start ([1-9] | [1-2][0-6])$", command_input)
      if start_match_flex:
        (start_cmd, dim) = command_input.split(' ')
        this_game.board = ttt_rep.TTT_Board(int(dim))
        board = this_game.board
      else:
        # Default to 3 x 3 dimension
        this_game.board = ttt_rep.TTT_Board(3)
        board = this_game.board
      return board.__str__()
    elif display_match:
      if board == None:
        return "```Cannot display board before starting game. Type '/ttt start DIM' to play new game.```\n" + board.__str__()
      return board.__str__()
    # This definition was placed here because we cannot access board.MAX_FILE until after "start" call
    if board.NUM_ROWS < 10:
      move_match = re.match("^move [a-" + board.MAX_FILE + "] [1-" + str(board.NUM_ROWS) + "]$", command_input)
    else:
      dim_str = str(board.NUM_ROWS)
      dim_first_dig = dim_str[0]
      dim_sec_dig = dim_str[1]
      move_match = re.match("^move [a-" + board.MAX_FILE + "] [1-" + dim_first_dig + ']' + "[0-" + dim_sec_dig + "]$", command_input)
    # Make move
    if move_match:
      if board == None:
        return "```Cannot make move before starting game. Type '/ttt start DIM' to play new game.```\n" + board.__str__()

      (move_cmd, fil_str, rnk_str) = command_input.split(' ')
      rnk = int(rnk_str)
      print "fil:", fil_str
      print "rnk:", rnk
      # Check if this valid file and rank
      if (0 <= board.file_to_rep(fil_str) < board.NUM_COLS) and (0 <= board.rank_to_rep(rnk) < board.NUM_ROWS):
        this_game.make_move(fil_str, rnk, 'x')
        return board.__str__()
      else:
        return "```Position (FILE, RANK) is out of bounds! Try again.```\n" + board.__str__()
    elif help_match:
      manual = open("ttt_manual.txt", 'r')
      return manual.read()
    else:
      return "```Illegal command! Type '/ttt help' for legal commands.```\n" + board.__str__()
  return "OK"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='', port=port)
