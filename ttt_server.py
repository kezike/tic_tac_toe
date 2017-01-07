import os
import re
import ttt_game
import ttt_rep
from slackclient import SlackClient
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify, abort

app = Flask(__name__)

HOST = "/kayode-ezike-ttt.herokuapp.com"
PORT = 5000
APP_TOKEN = os.environ["APP_TOKEN"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
slack_client = SlackClient(OAUTH_TOKEN)

this_game = ttt_game.TTT_Game()

# Convert Slack username to user id
def uname_to_uid(uname):
  user_list_res = slack_client.api_call("users.list")
  if user_list_res["ok"]:
    members = users_list_res["members"]
    for member in members:
      if member["name"] == uname:
        return member["id"]
    return "No such user!"
  return "Unable to authenticate!"

# Specifies response to start/restart command
def start_handler(cmd_input): 
  start_response = ""
  board = this_game.board 
  # Regex for invoking default-size board (3 x 3)
  start_and_restart_match = re.match("^(re)?start @[a-z0-9][a-z0-9._-]*$", cmd_input)
  # Regex for invoking configurable-size board
  start_and_restart_flex_match = re.match("^(re)?start ([1-9]|[1-2][0-6]) @[a-z0-9][a-z0-9._-]*$", cmd_input)
  if start_and_restart_match:
    exact_start_match = re.match("^start @[a-z0-9][a-z0-9._-]*$", cmd_input)
    if exact_start_match:
      # Check if game is already in progress
      # TODO - Check this from db
      if board != None:
        return "```Game already in progress! Type '/ttt restart' to start a new game.```"
    else:
      # End current game and start new game
      # TODO - Update db with flushed board and features and setup new board and features
      start_response = "```Ending current game and starting new game...```\n"
    # Default to 3 x 3 dimension
    (start_and_restart_cmd, uname_handle) = cmd_input.split(' ')
    uname = uname_handle.split('@')[1]
    uid = uname_to_uid(uname)
    start_response += "```Challenging " + uname + '(' + uid + ')' + "to game of Tic Tac Toe...```\n"
    this_game.board = ttt_rep.TTT_Board(3)
    board = this_game.board
  elif start_and_restart_flex_match:
    exact_start_flex_match = re.match("^start ([1-9]|[1-2][0-6])$", cmd_input)
    if exact_start_flex_match:
      # Check if game is already in progress
      # TODO - Check this from db
      if board != None:
        return "```Game already in progress! Type '/ttt restart' to start a new game.```"
    else:
      # End current game and start new game
      # TODO - Update db with flushed board and features and setup new board and features
      start_response = "```Ending current game and starting new game with desired configuration...```\n"
    # Use desired board configuration
    (start_and_restart_cmd, dim, uname_handle) = cmd_input.split(' ')
    uname = uname_handle.split('@')[1]
    uid = uname_to_uid(uname)
    start_response += "```Challenging " + uname + '(' + uid + ')' + "to game of Tic Tac Toe...```\n"
    this_game.board = ttt_rep.TTT_Board(int(dim))
    board = this_game.board
  else:
    # Command contains "start", but is not of a legal format
    return "```Illegal command format! Type '/ttt help' for legal command formatting.```"
  start_response += board.__str__()
  return start_response

# Specifies response to move command
def move_handler(cmd_input): 
  board = this_game.board
  turn_rep = this_game.turn_rep
  # Confirm from user info in request payload
  turn = this_game.rep_to_piece(turn_rep)
  (move_cmd, fil_rnk_str) = cmd_input.split(' ')
  fil_str = fil_rnk_str[0]
  rnk_str = fil_rnk_str[1:]
  rnk = int(rnk_str)
  # Check if file and rank globally in bounds (within a-z and 1-26)
  move_bounds_match = re.match("^move [a-z]([1-9]|[1-2][0-6])$", cmd_input)
  if not move_bounds_match:
    return "```Position (FILE, RANK) is out of bounds! a <= FILE <= max(a, min(z, MAX_FILE)), where MAX_FILE is the largest lexicographical letter for the board's dimension.```"
  # Check if file and rank locally in bounds (within board dimensions)
  dim_str = str(board.NUM_ROWS)
  if board.NUM_ROWS < 10:
    move_bounds_match = re.match("^move [a-" + board.MAX_FILE + "][1-" + dim_str + "]$", cmd_input)
  else:
    dim_first_dig = dim_str[0]
    dim_sec_dig = dim_str[1]
    move_bounds_match = re.match("^move [a-" + board.MAX_FILE + "][1-" + dim_first_dig + ']' + "[0-" + dim_sec_dig + "]$", cmd_input)
  if not move_bounds_match:
    return "```Position (FILE, RANK) is out of bounds! a <= FILE <= max(a, min(z, MAX_FILE)), where MAX_FILE is the largest lexicographical letter for the board's dimension.```"
  this_game.make_move(fil_str, rnk, turn)
  return board.__str__()

@app.route('/', methods=['POST'])
def ttt_handler():
  token = request.form.get('token', None)
  command = request.form.get('command', None)
  command_input = request.form.get('text', None)

  # Validate parameters
  if not token or token != APP_TOKEN:
    abort(400)
    return jsonify({
      "response_type": "ephemeral",
      "text": "Your app is not entitled to access the '/ttt' bot! :P"
    })
  board = this_game.board
  turn_rep = this_game.turn_rep
  # Confirm from user info in request payload
  turn = this_game.rep_to_piece(turn_rep)
  if command == "/ttt":
    start_match = re.search("start", command_input)
    display_match = re.match("^display$", command_input) 
    move_match = re.match("^move [a-z]\d+$", command_input)
    end_match = re.match("^end$", command_input)
    help_match = re.match("^help$", command_input)
    # Start game
    if start_match:
      # TODO - Check if game already exists for channel
      # If not, set caller's piece to 'X',
      # set opponent's piece to 'O', and display board
      return start_handler(command_input)
    # Display board
    elif display_match:
      if board == None:
        return "```Cannot display board before starting game. Type '/ttt start [DIM]' (where 1 <= DIM <= 26) to play a new game.```"
      return board.__str__()
    # Make move
    elif move_match:
      if board == None:
        return "```Cannot make move before starting game. Type '/ttt start [DIM]' (where 1 <= DIM <= 26) to play a new game.```"
      return move_handler(command_input)
    # End game
    elif end_match:
      if board == None:
        return "```Cannot end game before starting game. Type '/ttt start [DIM]' (where 1 <= DIM <= 26) to play a new game.```"
      # TODO - Update db with flushed board and features
      return "```Game Ended! Thanks for playing Tic Tac Toe :}```"
    # Display manual
    elif help_match:
      manual = open("ttt_manual.txt", 'r')
      return manual.read()
    else:
      return "```Illegal command format! Type '/ttt help' for legal command formatting.```"
  return "OK"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='', port=port)
