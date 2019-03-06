from copy import deepcopy

class Player:
  def __init__(self, name: str, signature: int):
    self.name = name
    self.signature = signature

  def __str__(self):
    return f'{self.name} won! (with signature: {self.signature}).'

class Board:
  def __init__(self):
    self.width = 7
    self.height = 6
    self.holes = [0] * (self.width * self.height)

  def get_hole(self, x: int, y: int):
    return self.holes[x + (y * self.width)]

  def set_hole(self, x: int, y: int, player: Player):
    self.holes[x + (y * self.width)] = player.signature

  def set_column(self, column: int, player: Player):
    for row in reversed(range(self.height)):
      if self.get_hole(column, row) == 0:
        return self.set_hole(column, row, player)

  def get_possible_columns(self):
    possible_columns = []
    for column in range(7):
      if self.get_hole(column, 0) is 0:
        possible_columns.append(column)
    return possible_columns
  
  def __str__(self):
    board_representation = ""
    for y in range(self.height):
      for x in range(self.width):
        board_representation += '{:2} '.format(str(self.get_hole(x, y)))
      board_representation += '\n'
    return board_representation

class ConnectFour:
  def __init__(self):
    self.board = Board()

  def has_won(self, player: Player):
    # reference: https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function
    board_width = self.board.width
    board_height = self.board.height
    player_signature = player.signature

    # check horizontal spaces
    for x in range(board_width):
        for y in range(board_height - 3):
            if (self.board.get_hole(x, y) == player_signature 
            and self.board.get_hole(x+1, y) == player_signature 
            and self.board.get_hole(x+2, y) == player_signature 
            and self.board.get_hole(x+3, y) == player_signature):
                return True

    # check vertical spaces
    for x in range(board_width):
        for y in range(board_height - 3):
            if (self.board.get_hole(x, y) == player_signature 
            and self.board.get_hole(x, y+1) == player_signature 
            and self.board.get_hole(x, y+2) == player_signature 
            and self.board.get_hole(x, y+3) == player_signature):
                return True

    # check / diagonal spaces
    for x in range(board_width - 3):
        for y in range(3, board_height):
            if (self.board.get_hole(x, y) == player_signature 
            and self.board.get_hole(x+1, y-1) == player_signature 
            and self.board.get_hole(x+2, y-2) == player_signature 
            and self.board.get_hole(x+3, y-3) == player_signature):
                return True

    # check \ diagonal spaces
    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if (self.board.get_hole(x, y) == player_signature 
            and self.board.get_hole(x+1, y+1) == player_signature 
            and self.board.get_hole(x+2, y+2) == player_signature 
            and self.board.get_hole(x+3, y+3) == player_signature):
                return True
    
    return False
  
  def is_draw(self):
    return 0 not in self.board.holes

  def can_move(self, column: int):
    return self.board.get_hole(column, 0) is 0

  def possible_boards(self, player: Player):
    """
    Returns a list of (column, board)
    """
    temp_board = deepcopy(self.board)
    column_and_boards = []
    for column in range(self.board.width):
      if (self.can_move(column)):
        self.move(player, column)
        column_and_boards.append((column, self.board))
        self.board = deepcopy(temp_board)
    return column_and_boards

  def move(self, player: Player, column: int):
    if self.can_move(column):
      self.board.set_column(column, player)

  def __str__(self):
    return self.board.__str__()

if __name__ == '__main__':
  connect_four = ConnectFour()
  first_player = Player('vince', 1)
  second_player = Player('jort', -1)

  print(connect_four.board)
  connect_four.move(first_player, 0)
  connect_four.move(first_player, 0)
  connect_four.move(first_player, 0)
  connect_four.move(first_player, 0)
  connect_four.move(first_player, 0)
  print(connect_four.board)

  # for x in range(connect_four.board.width):
  #   for y in range(connect_four.board.height):
  #     connect_four.board.set_hole(x, y, first_player)

  # print(connect_four.can_set_hole(0))
  # print(connect_four.has_won(second_player))