import string

ALPHA = string.ascii_lowercase
NUM_LETTERS = len(ALPHA)

# Represents a cell in a tic tac toe board
class TTT_Cell:
  def __init__(self):
    self.value = ' '

  def insert(self, val):
    self.value = val

  def __str__(self):
    return '|', self.value, '|'

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
    for i in xrange(self.NUM_ROWS):
      for j in xrange(self.NUM_COLS):
        self.cells.append(TTT_Cell())

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
        self.row_delim += "+"
    self.row_delim += '|'

    # Cache printed board
    self.printed_board = ""
    for i in xrange(self.NUM_ROWS):
      self.printed_board += str(self.NUM_ROWS - i) + ' '
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
    # TODO - assert that (row, col) is within board bounds
    # TODO - assert that piece has not already been inserted at (row, col)
    self.get_cell(fil, rnk).insert(val)    
    self.state_changed = True

  def __str__(self):
    if not self.state_changed:
      return self.printed_board
    self.printed_board = ""
    for i in xrange(self.NUM_ROWS):
      self.printed_board += str(self.NUM_ROWS - i) + ' '
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
    self.state_changed = False 
    return self.printed_board

# Tic Tac Toe
ttt_board = TTT_Board()
print "Tic Tac Toe\n", ttt_board
ttt_board.insert("b", 3, "O")
print "Tic Tac Toe\n", ttt_board
