from connect_four import ConnectFour, Board, Player
from random import choice
from copy import copy

import numpy as np
np.set_printoptions(linewidth=500)

"""
Settings
"""
AMOUNT_TO_CREATE = 100000

class StateAfterMove:
  def __init__(self, board: Board, player: Player, column_played: int, game_won: Player):
    self.board = board
    self.player = player
    self.column_played = column_played
    self.game_won = game_won

  def __str__(self):
    return f"{np.array(self.board.get_one_hot_array(self.player))};{self.player.signature};{self.column_played};{True if self.game_won else False}"

if __name__ == "__main__":
  games_created = 0
  amount_bot_won = 0
  amount_opposite_won = 0
  amount_draws = 0
  with open(f"../data/data_generated/data_win_classify_connect_four_game_{AMOUNT_TO_CREATE}.txt", "w") as win_classify_file:
    # file header
    win_classify_file.write(f"board representation;signature;column_played;game_ended;bot_won\n")
      
    bot = Player("Bot", 'A')
    opposite = Player("Opposite", 'B')
    while (games_created < AMOUNT_TO_CREATE):
      connect_four = ConnectFour(bot, opposite)
      all_states = list()
      while True:
        column_to_play = choice(connect_four.board.get_possible_columns())
        connect_four.move(column_to_play)

        state_after_move = StateAfterMove(copy(connect_four.board), bot, column_to_play, connect_four.has_won())

        all_states.append(state_after_move)
        
        won_player = connect_four.has_won()
        # Stop if game is won by one of the two players
        if (won_player is not None):
          for state in all_states:
            win_classify_file.write(f"{state};{1 if won_player is bot else 0}\n")

          if (won_player is bot):
            amount_bot_won += 1
          else:
            amount_opposite_won += 1
          break
        # Stop if the game ended in a draw
        elif connect_four.is_draw():
          amount_draws += 1
          for state in all_states:
            win_classify_file.write(f"{state};{0.5}\n")
          break

      games_created += 1
      if games_created % 1000 is 0:
        print(f"progress: {games_created}/{AMOUNT_TO_CREATE}.")

  print(f"Games won by bot:{amount_bot_won}. Games won by opposite:{amount_opposite_won}. Games ended in draw: {amount_draws}")