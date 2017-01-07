import string

ALPHA = string.ascii_lowercase
NUM_LETTERS = len(ALPHA)
INF = float("inf")

# Represents a cell in a tic tac toe board
class TTT_Cell:
  def __init__(self):
    self.value = ' '

  def insert(self, val):
    self.value = val

  def __str__(self):
    return '|', self.value, '|'

# Represents a section in a tic tac toe board
class TTT_Section:
  def __init__(self):
    # bit array representing 'X's (1), 'O's (0), and null (infinity)
    self.cells = []
    self.NUM_CELLS = INF
    self.num_insertions = 0
    self.last_insertion = INF
    self.matches = True

  def insert(self, val):
    if val == 'X':
      self.cells.append(1)
      self.num_insertions += 1
      self.matches = self.matches and (self.last_insertion == 1 or self.last_insertion == INF)
      self.last_insertion = 1
    elif val == 'O':
      self.cells.append(0)
      self.num_insertions += 1
      self.matches = self.matches and (self.last_insertion == 0 or self.last_insertion == INF)
      self.last_insertion = 0
  
  def is_complete(self):
    # assumes NUM_CELLS will be set to nonzero value before called
    return self.matches and self.num_insertions == self.NUM_CELLS

  def __str__(self):
    # TODO
    pass

# Represents a row in a tic tac toe board
class TTT_Row(TTT_Section):
  def __str__(self):
    # TODO
    pass

# Represents a columnn in a tic tac toe board
class TTT_Col(TTT_Section):
  def __str__(self):
    # TODO
    pass

# Represents a diagonal in a tic tac toe board
class TTT_Diag(TTT_Section):
  def __str__(self):
    # TODO
    pass

# Represents a tic tac toe board
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
class TTT_Board:
  def __init__(self, dim=3):
    self.NUM_ROWS = dim
    self.NUM_COLS = dim
    # Turn represented as boolean,
    # where True = X and False = O
    self.rep_to_pce = {True: 'X', False: 'O'}
    self.turn_rep = True
    # Text above board
    self.INITIAL_HEADER = "```Welcome To Tic Tac Toe!\nTurn: X"
    self.STEADY_STATE_HEADER = "```Tic Tac Toe\nTurn:"
    self.header = self.INITIAL_HEADER

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
      row = TTT_Row()
      row.NUM_CELLS = self.NUM_COLS
      for j in xrange(self.NUM_COLS):
        cell = TTT_Cell()
        self.rows.append(row)
        if j >= len(self.cols):
          col = TTT_Col()
          col.NUM_CELLS = self.NUM_ROWS
          self.cols.append(col)
        if i == j:
          if len(self.diags) == 0:
            diag = TTT_Diag()
            diag.NUM_CELLS = self.NUM_COLS
            self.diags.append(diag)
        elif i + j == self.NUM_ROWS - 1:
          if len(self.diags) == 1:
            diag = TTT_Diag()
            diag.NUM_CELLS = self.NUM_COLS
            self.diags.append(diag)
        self.cells.append(cell)

    # Convert file to cell index
    # (max file is 26 for alphabet)
    file_iter = 0
    self.fil_to_rep = {}
    while file_iter < NUM_LETTERS:
      self.fil_to_rep[ALPHA[file_iter]] = file_iter
      file_iter += 1

    # Convert cell index to file
    self.rep_to_fil = {}
    for (fil, rep) in self.fil_to_rep.iteritems():
      self.rep_to_fil[rep] = fil

    # Calculate row delimiter in printed board: |---+---+---|
    self.row_delim = '|' 
    for j in xrange(self.NUM_COLS):
      self.row_delim += "---"
      if j != self.NUM_COLS - 1:
        self.row_delim += '+'
    self.row_delim += '|'

    # Cache printed board
    # Ticks, underscores, and asterisks are for Slack formatting
    self.printed_board = self.header
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.printed_board += rank_str
      if len(rank_str) == 1:
        self.printed_board += ' '
      for j in xrange(self.NUM_COLS):
        self.printed_board += '|   '
        if j == self.NUM_COLS - 1:
          self.printed_board += '|'
          if i != self.NUM_ROWS - 1:
            self.printed_board += '\n' + "  " + self.row_delim + '\n'
    file_delim = "   "
    file_string = "\n "
    for j in xrange(self.NUM_COLS):
      file_string += file_delim + self.rep_to_fil[j]
    self.printed_board += file_string
    self.printed_board += "```"
    self.state_changed = False
  
    # Configure square dimension of board
    self.MAX_FILE = self.rep_to_fil[self.NUM_ROWS - 1]

  # Converts boolean to turn piece
  def rep_to_piece(self, piece_rep):
    return self.rep_to_pce[piece_rep]

  # Converts file to cell index
  # (max file is 26 for alphabet)
  def file_to_rep(self, fil):
    # TODO - assert valid file
    return self.fil_to_rep[fil]

  # Converts rank to cell index
  def rank_to_rep(self, rnk):
    # TODO - assert valid rank
    return self.NUM_ROWS - rnk

  # Converts cell index to file
  def rep_to_file(self, rep):
    return self.rep_to_fil[rep]

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
    self.header = self.STEADY_STATE_HEADER
    self.state_changed = True

  def __str__(self):
    if not self.state_changed:
      return self.printed_board 
    self.printed_board = self.header
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.printed_board += rank_str
      if len(rank_str) == 1:
        self.printed_board += ' '
      for j in xrange(self.NUM_COLS):
        self.printed_board += '| ' + self.get_cell(self.rep_to_file(j), self.rep_to_rank(i)).value + ' '
        if j == self.NUM_COLS - 1:
          self.printed_board += '|'
          if i != self.NUM_ROWS - 1:
            self.printed_board += '\n' + "  " + self.row_delim + '\n'
    file_delim = "   "
    file_string = "\n "
    for j in xrange(self.NUM_COLS):
      file_string += file_delim + self.rep_to_file(j)
    self.printed_board += file_string
    self.printed_board += "```"
    self.state_changed = False 
    return self.printed_board
