import os
import re
import ttt_rep
import logging
from slackclient import SlackClient
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

this_game = None
this_board = None

import ttt_util
UTIL = ttt_util.Util()
HOST = "/kayode-ezike-ttt.herokuapp.com"
PORT = 5000
APP_TOKEN = os.environ["APP_TOKEN"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
SLACK_CLIENT = SlackClient(OAUTH_TOKEN)
USER_NOT_FOUND_ERROR = "```No such user in this Slack!```"
USER_NOT_IN_CHANNEL_ERROR = "```No such user in this channel!```"
WRONG_USER_ERROR = "```It is not your turn to play! Please wait for your opponent to make their move.```"
OAUTH_ERROR = "```You are not authenticated to use this Slack API call! Configure your application environment with proper permissions.```"

# Convert Slack username to user id
def uname_to_uid(uname):
  user_list_res = SLACK_CLIENT.api_call("users.list")
  if user_list_res["ok"]:
    members = user_list_res["members"]
    for member in members:
      if member["name"] == uname:
        return member["id"]
    return USER_NOT_FOUND_ERROR
  # Unable to authenticate
  return OAUTH_ERROR

# Convert Slack user id to username
def uid_to_uname(uid):
  user_info_res = SLACK_CLIENT.api_call("users.info", user=uid)
  if user_info_res["ok"]:
    return user_info_res["user"]["name"]
  # Unable to authenticate
  return OAUTH_ERROR

# Check if user is a member of a Slack channel
def user_in_channel(uid, ch_id):
  channel_info_res = SLACK_CLIENT.api_call("channels.info", channel=ch_id)
  if channel_info_res["ok"]:
    return uid in channel_info_res["channel"]["members"]
  return OAUTH_ERROR

# Specifies response to start/restart command
def start_handler(cmd_input, own_uid, ch_id):
  player_x = ttt_rep.Player(True, own_uid)
  player_y = None # determined below
  own_uname = uid_to_uname(own_uid)
  start_response = "```Turn: X (@" + own_uname + ")\n"
  # Regex for invoking default-size board (3 x 3)
  start_and_restart_match = re.match("^(re)?start @[a-z0-9][a-z0-9._-]*$", cmd_input)
  # Regex for invoking configurable-size board
  start_and_restart_flex_match = re.match("^(re)?start ([1-9]|[1-2][0-6]) @[a-z0-9][a-z0-9._-]*$", cmd_input)
  if start_and_restart_match:
    exact_restart_match = re.match("^restart @[a-z0-9][a-z0-9._-]*$", cmd_input)
    if exact_restart_match:
      # End current game and start new game
      start_response = "```Ending current game and starting new game...```\n" + start_response
    # Default to 3 x 3 dimension
    (start_and_restart_cmd, uname_handle) = cmd_input.split(' ')
    opp_uname = uname_handle.split('@')[1]
    opp_uid = uname_to_uid(opp_uname)
    player_y = ttt_rep.Player(False, opp_uid)
    if not user_in_channel(opp_uid, ch_id):
      return USER_NOT_IN_CHANNEL_ERROR
    start_response = "```@" + own_uname + " (X) is challenging @" + opp_uname + " (O) " + "to a game of Tic Tac Toe...```\n" + start_response
    global this_game
    this_game = ttt_rep.Game(own_uid, opp_uid, ch_id, True)
    turn_rep = this_game.turn_rep
    # TODO - Confirm from user info in request payload
    turn = UTIL.rep_to_piece(turn_rep) 
    this_game.board = ttt_rep.Board(3)
    global this_board
    this_board = this_game.board
  elif start_and_restart_flex_match:
    exact_restart_flex_match = re.match("^restart ([1-9]|[1-2][0-6])$", cmd_input)
    if exact_restart_flex_match:
      # End current game and start new game
      start_response = "```Ending current game and starting new game with desired configuration...```\n" + start_response
    # Use desired board configuration
    (start_and_restart_cmd, dim, uname_handle) = cmd_input.split(' ')
    opp_uname = uname_handle.split('@')[1]
    opp_uid = uname_to_uid(opp_uname)
    player_y = ttt_rep.Player(False, opp_uid)
    if not user_in_channel(opp_uid, ch_id):
      return USER_NOT_IN_CHANNEL_ERROR
    start_response = "```@" + uid_to_uname(own_uid) + " (X) is challenging @" + opp_uname + " (O) " + "to a game of tic tac toe...```\n" + start_response
    global this_game
    this_game = ttt_rep.Game(own_uid, opp_uid, ch_id, True)
    turn_rep = this_game.turn_rep
    # TODO - Confirm from user info in request payload
    turn = UTIL.rep_to_piece(turn_rep) 
    this_game.board = ttt_rep.Board(int(dim))
    global this_board
    this_board = this_game.board
  else:
    # Command contains "start", but is not of a legal format
    return "```Illegal command format! Type '/ttt help' for legal command formatting.```"
  start_response += this_board.__str__()
  return start_response

# Specifies response to move command
def move_handler(cmd_input, own_uid, ch_id):
  global this_game
  global this_board
  this_board = this_game.board
  piece_rep = this_game.turn_rep
  current_piece = UTIL.rep_to_piece(piece_rep)
  current_turn_uname = None
  if piece_rep:
    current_turn_uname = uid_to_uname(this_game.player_id_x)
  else:
    current_turn_uname = uid_to_uname(this_game.player_id_o)
  (move_cmd, fil_rnk_str) = cmd_input.split(' ')
  fil_str = fil_rnk_str[0]
  rnk_str = fil_rnk_str[1:]
  rnk = int(rnk_str)
  # Check if file and rank globally in bounds (within a-z and 1-26)
  move_bounds_match = re.match("^move [a-z]([1-9]|[1-2][0-6])$", cmd_input)
  if not move_bounds_match:
    return "```Position (FILE, RANK) is out of bounds! a <= FILE <= max(a, min(z, MAX_FILE)), where MAX_FILE is the largest lexicographical letter for the board's dimension.```"
  # Check if file and rank locally in bounds (within board dimensions)
  dim_str = str(this_board.NUM_ROWS)
  if this_board.NUM_ROWS < 10:
    move_bounds_match = re.match("^move [a-" + this_board.MAX_FILE + "][1-" + dim_str + "]$", cmd_input)
  else:
    dim_first_dig = dim_str[0]
    dim_sec_dig = dim_str[1]
    move_bounds_match = re.match("^move [a-" + this_board.MAX_FILE + "][1-" + dim_first_dig + ']' + "[0-" + dim_sec_dig + "]$", cmd_input)
  if not move_bounds_match:
    return "```Position (FILE, RANK) is out of bounds! a <= FILE <= max(a, min(z, MAX_FILE)), where MAX_FILE is the largest lexicographical letter for the board's dimension.```"
  # Confirm from user info in request payload
  this_game.make_move(fil_str, rnk, piece)
  if this_game.is_over():
    outcome = this_game.report_outcome()
    this_game = None
    this_board = None
    if outcome == None:
      return "```Game Over! Cat's Game - both players win!```"
    return "```Game Over! Congratulations " + '@' + current_turn_uname + " (Player " + piece + ")! You have won the game!```"
  new_piece_rep = this_game.turn_rep
  new_piece = UTIL.rep_to_piece(new_piece_rep)
  new_turn_uname = None
  if new_piece_rep:
    new_turn_uname = uid_to_uname(this_game.player_id_x)
  else:
    new_turn_uname = uid_to_uname(this_game.player_id_o)
  move_response = "```Turn: " + new_piece + " (@" + new_turn_uname + ")\n" + this_board.__str__()
  return move_response

@app.route('/', methods=['POST'])
def ttt_handler():
  token = request.form.get('token', None)
  command = request.form.get('command', None)
  command_input = request.form.get('text', None)
  user_id = request.form.get('user_id', None)
  ch_id = request.form.get('channel_id', None)

  # Validate parameters
  if not token or token != APP_TOKEN:
    abort(400)
    return jsonify({
      "response_type": "ephemeral",
      "text": "Your app is not entitled to access the '/ttt' bot! :P"
    })
  global this_game
  global this_board
  if command == "/ttt":
    start_match = re.search("start", command_input)
    display_match = re.match("^display$", command_input) 
    move_match = re.match("^move [a-z]\d+$", command_input)
    end_match = re.match("^end$", command_input)
    help_match = re.match("^help$", command_input)
    # Start game
    if start_match:
      if this_board != None:
        return "```Game already in progress in current channel! Run '/ttt display' to display status of current game or '/ttt restart @SLACK_USERNAME' to start a new game.```"
      return start_handler(command_input, user_id, ch_id)
    # Display board
    elif display_match:
      if this_board == None:
        return "```Cannot display board before starting game. Type '/ttt start [DIM] @SLACK_USERNAME' (where 1 <= DIM <= 26) to play a new game.```"
      turn_rep = this_game.turn_rep
      turn_uname = None
      if turn_rep:
        turn_uname = uid_to_uname(this_game.player_id_x)
      else:
        turn_uname = uid_to_uname(this_game.player_id_o)
      display_response = "```Turn: " + UTIL.rep_to_piece(turn_rep) + " (@" + turn_uname + ")\n" + this_board.__str__()
      return display_response
    # Make move
    elif move_match:
      if this_board == None:
        return "```Cannot make move before starting game. Type '/ttt start [DIM] @SLACK_USERNAME' (where 1 <= DIM <= 26) to play a new game.```"
      return move_handler(command_input, user_id, ch_id)
    # End game
    elif end_match:
      if this_board == None:
        return "```Cannot end game before starting game. Type '/ttt start [DIM] @SLACK_USERNAME' (where 1 <= DIM <= 26) to play a new game.```"
      this_game = None
      this_board = None
      return "```Game Ended! Thanks for playing Tic Tac Toe :}```"
    # Display /ttt docs
    elif help_match:
      docs = open("ttt_docs.txt", 'r')
      return docs.read()
    else:
      return "```Illegal command format! Type '/ttt help' for legal command formatting.```"
  return "OK"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='', port=port)
