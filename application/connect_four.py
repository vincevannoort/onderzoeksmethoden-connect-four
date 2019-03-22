from copy import deepcopy
from random import choice
from termcolor import colored
import numpy as np

class Player:
  def __init__(self, name: str, signature: int):
    self.name = name
    self.signature = signature

  def __str__(self):
    return self.name

class Board:
  def __init__(self):
    self.width = 7
    self.height = 6
    self.holes = [0] * (self.width * self.height)

  def get_hole(self, x: int, y: int):
    if x >= self.width or x < 0 or y >= self.height or y < 0:
      raise Exception(f"Index ({x},{y}) is outside of the connect four board.")
    return self.holes[x + (y * self.width)]

  def set_hole(self, x: int, y: int, player: Player):
    if x >= self.width or x < 0 or y >= self.height or y < 0:
      raise Exception(f"Index ({x},{y}) is outside of the connect four board.")
    self.holes[x + (y * self.width)] = player.signature

  def set_column(self, column: int, player: Player):
    for row in reversed(range(self.height)):
      if self.get_hole(column, row) == 0:
        return self.set_hole(column, row, player)

  def get_possible_columns(self):
    possible_columns = []
    for column in range(self.width):
      if self.get_hole(column, 0) is 0:
        possible_columns.append(column)
    return possible_columns

  def get_possible_columns_as_one_hot_array(self):
    possible_columns = self.get_possible_columns()
    possible_columns_one_hot_array = np.zeros(7)
    for possible_column in possible_columns:
      np.put(possible_columns_one_hot_array, possible_column, 1)
    return possible_columns_one_hot_array

  def print_with_colors(self, first_player_signature, second_player_signature):
    board_representation = " 1  2  3  4  5  6  7 \n"
    for y in range(self.height):
      for x in range(self.width):
        signature = self.get_hole(x, y)
        board_representation += f"({(colored(signature, 'red') if signature is first_player_signature else colored(signature, 'green')) if signature is not 0 else ' '})"
      board_representation += '\n'
    print(board_representation)

  def get_one_hot_array(self, player: Player):
    def hole_to_array(hole, player: Player):
      """
      Generates one hot array from hole.
      Empty hole        -> [1, 0, 0] 
      Given player      -> [0, 1, 0] 
      Not given player  -> [0, 0, 1]
      """
      return [
        1 if hole is 0 else 0, # hole empty
        1 if hole is player.signature else 0, # hole self
        1 if hole is not player.signature and hole is not 0 else 0, # hole enemy
      ]

    board_representation = []
    for hole in self.holes:
      board_representation += hole_to_array(hole, player)
    return board_representation

  def __str__(self):
    board_representation = ""
    for y in range(self.height):
      for x in range(self.width):
        signature = self.get_hole(x, y)
        board_representation += f"({signature if signature is not 0 else ' '})"
      board_representation += '\n'
    return board_representation

class ConnectFour:
  def __init__(self, first_player: Player, second_player: Player):
    self.board = Board()
    self.first_player = first_player
    self.second_player = second_player
    self.current_player = choice([first_player, second_player])

  def reset(self):
    self.__init__(self.first_player, self.second_player)

  def switch_player(self, player: Player):
    return self.second_player if self.current_player is self.first_player else self.first_player

  def has_won(self):
    # reference: https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function
    board_width = self.board.width
    board_height = self.board.height
    player = self.switch_player(self.current_player)
    player_signature = player.signature

    # check horizontal spaces
    for x in range(board_width - 3):
      for y in range(board_height):
        if (self.board.get_hole(x, y) == player_signature
        and self.board.get_hole(x+1, y) == player_signature
        and self.board.get_hole(x+2, y) == player_signature
        and self.board.get_hole(x+3, y) == player_signature):
          return player

    # check vertical spaces
    for x in range(board_width):
      for y in range(board_height - 3):
        if (self.board.get_hole(x, y) == player_signature
        and self.board.get_hole(x, y+1) == player_signature
        and self.board.get_hole(x, y+2) == player_signature
        and self.board.get_hole(x, y+3) == player_signature):
          return player

    # check / diagonal spaces
    for x in range(board_width - 3):
      for y in range(3, board_height):
        if (self.board.get_hole(x, y) == player_signature
        and self.board.get_hole(x+1, y-1) == player_signature
        and self.board.get_hole(x+2, y-2) == player_signature
        and self.board.get_hole(x+3, y-3) == player_signature):
          return player

    # check \ diagonal spaces
    for x in range(board_width - 3):
      for y in range(board_height - 3):
        if (self.board.get_hole(x, y) == player_signature
        and self.board.get_hole(x+1, y+1) == player_signature
        and self.board.get_hole(x+2, y+2) == player_signature
        and self.board.get_hole(x+3, y+3) == player_signature):
          return player

    return None

  def is_draw(self):
    return 0 not in self.board.holes

  def can_move(self, column: int):
    return self.board.get_hole(column, 0) is 0

  def possible_boards_columns(self, player: Player):
    """
    Returns a list of (column, board)
    """
    temp_board = deepcopy(self.board)
    column_and_boards = []
    for column in range(self.board.width):
      if (self.can_move(column)):
        self.fake_move(column)
        column_and_boards.append((column, self.board))
        self.board = deepcopy(temp_board)
    return column_and_boards

  def fake_move(self, column: int):
    if self.can_move(column):
      self.board.set_column(column, self.current_player)
    else:
      raise Exception("Board is full. No moves can be set.")

  def move(self, column: int):
    if self.can_move(column):
      self.board.set_column(column, self.current_player)
      self.current_player = self.switch_player(self.current_player)
    else:
      raise Exception("Board is full. No moves can be set.")


  def __str__(self):
    return self.board.__str__()

if __name__ == "__main__":
  connect_four = ConnectFour(Player("vince", 'A'), Player("jort", 'B'))
  print(connect_four.board)
  connect_four.move(0)
  connect_four.move(0)
