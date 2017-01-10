@singleton
class Util:
  def __init__(self):
    # Turn represented as boolean,
    # where True = X and False = O
    self.rep_to_pce = {True: 'X', False: 'O'}

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

  def rep_to_piece(self, piece_rep):
    return self.rep_to_pce[piece_rep]
