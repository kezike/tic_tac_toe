import ttt_rep

class TTT_Game:
  def __init__(self):
    self.board = ttt_rep.TTT_Board()
    self.turn = True

  def make_move(self, fil, rnk, val):
    self.board.insert(fil, rnk, val)
    # Now opponent's turn
    self.turn = not self.turn

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
''''
this_game = TTT_Game()
print this_game.board
if __name__ == "__main__":
  while not this_game.is_over():
    this_game.play()
'''
