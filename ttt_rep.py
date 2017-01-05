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
    # bit array representing 'x's (1), 'o's (0), and null (infinity)
    self.cells = []
    self.NUM_CELLS = INF
    self.num_insertions = 0
    self.last_insertion = INF
    self.matches = True

  def insert(self, val):
    if val == 'x':
      self.cells.append(1)
      self.num_insertions += 1
      self.matches = self.matches and (self.last_insertion == 1 or self.last_insertion == INF)
      self.last_insertion = 1
    elif val == 'o':
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
  def __init__(self):
    self.NUM_ROWS = 3
    self.NUM_COLS = 3

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
    while file_iter < self.NUM_COLS and file_iter < NUM_LETTERS:
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
    # I made changes to this part that may make it seem hard-coded,
    # but the truth is that due to differences in string output
    # between command-line and Slack (monospaced vs. "polyspaced").
    # For now, I store a blank board in a separate file and load it in,
    # but include the commented original logic for the future, should I
    # decide to truly scale this application to beyond 3x3, as was my
    # original intention, given other components of my design (ie. NUM_ROWS, NUM_COLS)
    """
    self.printed_board = "Tic Tac Toe\n"
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.printed_board += rank_str
      if len(rank_str) == 1:
        self.printed_board += ' '
      for j in xrange(self.NUM_COLS):
        self.printed_board += '|      '
        if j == 1:
          self.printed_board += ' '
        if j == self.NUM_COLS - 1:
          self.printed_board += '|'
          if i != self.NUM_ROWS - 1:
            self.printed_board += '\n' + "     " + self.row_delim + '\n'
    file_delim = "    "
    file_string = "\n    "
    for j in xrange(self.NUM_COLS):
      if j == 1:
        file_delim += '  '
      file_string += file_delim + self.rep_to_fil[j]
    self.printed_board += file_string
    """
    blank_board = open("ttt_blank_3_x_3.txt", 'r')
    self.printed_board = blank_board.read()
    self.state_changed = False

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
    # TODO - assert that fil and rnk are valid (may save for higher level)
    # TODO - assert that (fil, rnk) is within board bounds
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
    self.state_changed = True

  def __str__(self):
    if not self.state_changed:
      return self.printed_board
    # TODO - Configure following line
    # to report who's turn it is
    # Backticks are for formatting
    # text to be monospaced in Slack
    self.printed_board = "```\nTic Tac Toe\n"
    for i in xrange(self.NUM_ROWS):
      rank_str = str(self.NUM_ROWS - i)
      self.printed_board += rank_str
      if len(rank_str) == 1:
        self.printed_board += ' '
      for j in xrange(self.NUM_COLS):
        self.printed_board += '|   ' + self.get_cell(self.rep_to_file(j), self.rep_to_rank(i)).value + '   '
        if j == 1:
          self.printed_board += ' '
        if j == self.NUM_COLS - 1:
          self.printed_board += '|'
          if i != self.NUM_ROWS - 1:
            self.printed_board += '\n' + "     " + self.row_delim + '\n'
    file_delim = "    "
    file_string = "\n    "
    for j in xrange(self.NUM_COLS):
      if j == 1:
        file_delim += '  '
      file_string += file_delim + self.rep_to_file(j)
    self.printed_board += file_string
    self.printed_board += "\n```"
    self.state_changed = False 
    return self.printed_board

board = TTT_Board()
print board
