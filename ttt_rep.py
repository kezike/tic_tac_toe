from flask_sqlalchemy import SQLAlchemy
from ttt_app import db
import ttt_util

UTIL = ttt_util.Util()

# Represents a cell in a tic tac toe board
class Cell(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  value = db.Column(db.String(1))
  row = db.Column(db.Integer)
  col = db.Column(db.Integer)
  board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
  board = db.relationship("Board", back_populates="cells")

  def __init__(self, board, row, col, val):
    self.row = row
    self.col = col
    self.value = val
    self.board = board

  def insert(self, val):
    self.value = val

  def __repr__(self):
    return '|', self.value, '|'

  def __str__(self):
    return '|', self.value, '|'

# Represents a section in a tic tac toe board
class Section:
  def __init__(self, num_cells):
    # bit array representing 'X's (1), 'O's (0), and null (infinity)
    self.cells = []
    self.NUM_CELLS = num_cells
    self.num_insertions = 0
    # Special value representing the last value to be inserted into the section
    # Begins at 30 in the beginning because there will never be up to 30 pieces
    # considering that the max number of insertions is 26. However, when we encounter
    # this value, we can safely assume that this is the initial case, in which there
    # has not yet been any insertions
    self.last_insertion = 30
    self.matches = True

  def insert(self, val):
    if val == 'X':
      self.cells.append(1)
      self.num_insertions += 1
      self.matches = self.matches and (self.last_insertion == 1 or self.last_insertion == 30)
      self.last_insertion = 1
    elif val == 'O':
      self.cells.append(0)
      self.num_insertions += 1
      self.matches = self.matches and (self.last_insertion == 0 or self.last_insertion == 30)
      self.last_insertion = 0
  
  def is_complete(self):
    # assumes NUM_CELLS will be set to nonzero value before called
    return self.matches and self.num_insertions == self.NUM_CELLS

  def __str__(self):
    # TODO
    pass

# Represents a row in a tic tac toe board
class Row(Section):
  def __str__(self):
    # TODO
    pass

# Represents a columnn in a tic tac toe board
class Col(Section):
  def __str__(self):
    # TODO
    pass

# Represents a diagonal in a tic tac toe board
class Diag(Section):
  def __str__(self):
    # TODO
    pass

# Represents a square tic tac toe board
# File - letter
# Rank - number
"""
Tic Tac Toe
3 |   |   |   |
  |---+---+---|
2 |   |   |   |
  |---+---+---|
1 |   |   |   |
    a   b   c 
"""
class Board(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey("Game.id"))
  game = db.relationship("Game", back_populates="board")
  cells = db.relationship("Cell", order_by="Cell.row", back_populates="board")
  turn_rep = db.Column(db.Boolean)
  board_str = db.Column(db.String)

  def __init__(self, dim=3):
    self.DIM = dim
    self.NUM_ROWS = dim
    self.NUM_COLS = dim
    self.turn_rep = True
    '''
    # Text above board
    self.WELCOME_HEADER = "```Welcome To Tic Tac Toe!\nTurn: X"
    self.MAIN_HEADER = "```Tic Tac Toe\nTurn:"
    self.header = self.WELCOME_HEADER 
    '''
    
    # Stores tic tac toe moves thus far
    # (represented in row major form)
    self.cells = []
    # Stores rows of tic tac toe board
    self.rows = []
    # Stores columns of tic tac toe board
    self.cols = []
    # Stores diagonals of tic tac toe board
    # first elem reps NW-SE diag
    # second elem reps NE-SW diag
    self.diags = []
    # Setup rows, cols, and diags
    for i in xrange(self.NUM_ROWS):
      row = Row(self.NUM_COLS)
      for j in xrange(self.NUM_COLS):
        cell = Cell(self, i, j, ' ')
        db.session.add(cell)
        self.rows.append(row)
        if j >= len(self.cols):
          col = Col(self.NUM_ROWS)
          self.cols.append(col)
        if i == j:
          if len(self.diags) == 0:
            diag = Diag(self.NUM_COLS)
            self.diags.append(diag)
        elif i + j == self.NUM_ROWS - 1:
          if len(self.diags) == 1:
            diag = Diag(self.NUM_COLS)
            self.diags.append(diag)
        self.cells.append(cell)
    db.session.commit()

    # Calculate row delimiter in printed board: |---+---+---|
    self.row_delim = '|'
    for j in xrange(self.NUM_COLS):
      self.row_delim += "---"
      if j != self.NUM_COLS - 1:
        self.row_delim += '+'
    self.row_delim += '|'

    # Cache board string
    # Ticks, underscores, and asterisks are for Slack formatting
    self.board_str = ""
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.board_str += rank_str
      if len(rank_str) == 1:
        self.board_str += ' '
      for j in xrange(self.NUM_COLS):
        self.board_str += '|   '
        if j == self.NUM_COLS - 1:
          self.board_str += '|'
          if i != self.NUM_ROWS - 1:
            self.board_str += '\n' + "  " + self.row_delim + '\n'
    file_delim = "   "
    file_string = "\n "
    for j in xrange(self.NUM_COLS):
      file_string += file_delim + UTIL.rep_to_fil[j]
    self.board_str += file_string
    self.board_str += "```"
    self.state_changed = True
  
    # Configure square dimension of board
    self.MAX_FILE = UTIL.rep_to_fil[self.NUM_ROWS - 1]

  # Converts file to cell index
  # (max file is 26 for alphabet)
  def file_to_rep(self, fil):
    return UTIL.fil_to_rep[fil]

  # Converts rank to cell index
  def rank_to_rep(self, rnk):
    return self.NUM_ROWS - rnk

  # Converts cell index to file
  def rep_to_file(self, rep):
    return UTIL.rep_to_fil[rep]

  # Converts cell index to rank
  def rep_to_rank(self, rep):
    return self.NUM_ROWS - rep

  def get_cell(self, fil, rnk):
    return self.cells[(self.rank_to_rep(rnk) - 1) * self.NUM_COLS + self.file_to_rep(fil) - 1]

  def insert(self, fil, rnk, val):
    # TODO - assert that piece has not already been inserted at (fil, rnk)
    rank_rep = self.rank_to_rep(rnk)
    file_rep = self.file_to_rep(fil)
    self.rows[rank_rep].insert(val)
    self.cols[file_rep].insert(val)
    if rank_rep == file_rep:
      self.diags[0].insert(val)
    if rank_rep + file_rep == self.NUM_ROWS - 1:
      self.diags[1].insert(val)
    self.get_cell(fil, rnk).insert(val)    
    self.turn_rep = not self.turn_rep
    self.state_changed = True

  def __repr__(self):
    return "<Board %d x %d>" % (self.NUM_ROWS, self.NUM_COLS)

  def __str__(self):
    if not self.state_changed:
      return self.board_str
    self.board_str = ""
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.board_str += rank_str
      if len(rank_str) == 1:
        self.board_str += ' '
      for j in xrange(self.NUM_COLS):
        self.board_str += '| ' + self.get_cell(self.rep_to_file(j), self.rep_to_rank(i)).value + ' '
        if j == self.NUM_COLS - 1:
          self.board_str += '|'
          if i != self.NUM_ROWS - 1:
            self.board_str += '\n' + "  " + self.row_delim + '\n'
    file_delim = "   "
    file_string = "\n "
    for j in xrange(self.NUM_COLS):
      file_string += file_delim + self.rep_to_file(j)
    self.board_str += file_string
    self.board_str += "```"
    self.state_changed = False 
    return self.board_str

# Represents a game of tic tac toe
class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  player_id_x = db.Column(db.String)
  player_id_o = db.Column(db.String)
  channel_id = db.Column(db.String)
  board = db.relationship("Board", uselist=False, back_populates="Game")
  turn_rep = db.Column(db.Boolean)
  
  def __init__(self, pid_x, pid_o, ch_id, turn_rep):
    # Must initialize board with dimensions indicated
    # in game play or 3 x 3 if not indicated
    self.player_id_x = pid_x
    self.player_id_o = pid_o
    self.channel_id = ch_id
    self.turn_rep = turn_rep
    self.board = None
  
  def make_move(self, fil, rnk, val):
    self.board.insert(fil, rnk, val)
    # Now opponent's turn
    self.turn_rep = not self.turn_rep

  def is_over(self):
    board_rows = self.board.rows
    board_cols = self.board.cols
    board_diags = self.board.diags
    for row in board_rows:
      if row.is_complete():
        return True
    for col in board_cols:
      if col.is_complete():
        return True
    for diag in board_diags:
      if diag.is_complete():
        return True
    return False
  
# Represents a player of tic tac toe
class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  piece_rep = db.Column(db.Boolean)
  player_id = db.Column(db.String)

  def __init__(self, piece_rep, pid):
    self.piece_rep = piece_rep
    self.player_id = pid

  def __repr__(self):
    "<Player %r (@%r)>" % (UTIL.rep_to_piece(self.turn_rep), self.username)
