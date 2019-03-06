from connect_four import ConnectFour, Board, Player
from random import choice
from copy import copy

class MoveFromPlayer:
  def __init__(self, board: Board, player: Player, column_played: int, game_won: bool):
    self.board = board
    self.player = player
    self.column_played = column_played
    self.game_won = game_won

  def __str__(self):
    def hole_to_array(hole, player: Player):
      return [
        1 if hole is 0 else 0, # hole empty
        1 if hole is player.signature else 0, # hole self
        1 if hole is not player.signature and hole is not 0 else 0, # hole enemy
      ]

    board_representation = []
    for hole in self.board.holes:
      board_representation += hole_to_array(hole, self.player)

    return f'{board_representation};{self.player.signature};{self.column_played};{self.game_won}\n'

if __name__ == '__main__':
  amount_to_create = 50
  with open(f'../data/data_generated/connect-four-game-{amount_to_create}.txt', 'w') as file:
    for game in range(amount_to_create):
      connect_four = ConnectFour()
      first_player = Player('Vince', 'R')
      second_player = Player('Jort', 'G')
      current_player = first_player
      moves = dict()
      while(True):
        current_player = first_player if current_player is second_player else second_player
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if len(possible_columns) <= 0:
          break

        column_to_play = choice(connect_four.board.get_possible_columns())
        connect_four.move(current_player, column_to_play)

        # setup a dict of moves per player, since we only need the moves from the winning player
        move_from_player = MoveFromPlayer(copy(connect_four.board), current_player, column_to_play, connect_four.has_won(current_player))
        if current_player in moves:
          moves[current_player].append(move_from_player)
        else:
          moves[current_player] = [move_from_player]

        if (connect_four.has_won(current_player)):
          for move in moves[current_player]:
            file.write(str(move))
          break

      if game % 1000 is 0:
        print(f'progress: {game}/{amount_to_create}.')