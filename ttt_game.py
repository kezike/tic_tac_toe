import ttt_rep
# Tic Tac Toe Test Suite
ttt_board = ttt_rep.TTT_Board()
print "Tic Tac Toe\n", ttt_board
ttt_board.insert("b", 3, "o")
print "Tic Tac Toe\n", ttt_board

class TTT_Game:
  def __init__(self):
    self.board = ttt_rep.TTT_Board()
    self.turn = True

  def make_move(self, fil, rnk, val):
    # assert that it is player's turn
    if move != self.turn:
      # TODO - raise warning
      pass
    # TODO - assert that this is a valid move
    # Commit to move
    board.insert(fil, rnk, val)
    # Now opponent's turn
    self.turn = not self.turn

  def is_over(self):
    board_rows = board.rows
    board_cols = board.cols
    board_diags = board.diags
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

  def play():
    # TODO - accept input from users and invalidate input
    pass

this_game = TTT_Game()

if __name__ == "__main__":
  while not this_game.is_over():
    this_game.play()
