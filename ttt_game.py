import ttt_rep

class TTT_Game:
  def __init__(self):
    # Must initialize board with dimensions indicated
    # in game play or 3 x 3 if not indicated
    self.board = None
    self.rep_to_pce = {True:'x', False:'o'}
    self.turn_rep = True
  
  def rep_to_piece(self, piece_rep):
    return self.rep_to_pce[piece_rep]

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

  def play(self):
    # TODO - accept input from users and invalidate input
    pass
