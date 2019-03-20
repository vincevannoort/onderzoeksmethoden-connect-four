from connect_four import ConnectFour, Board, Player
from random import choice, shuffle
from copy import copy
import readchar
import os
import numpy as np
np.set_printoptions(linewidth = 300);

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class StateAfterMove:
  def __init__(self, board: Board, player: Player, column_to_play: int, game_won: bool):
    self.board = board
    self.player = player
    self.columns_to_play = np.zeros(7)
    np.put(self.columns_to_play, column_to_play, 1)
    self.game_won = game_won

  def __str__(self):
    return f'{np.array2string(np.array(self.board.get_one_hot_array(self.player)))};{self.player.signature};{np.array2string(self.columns_to_play)};{True if self.game_won else False}'

if __name__ == '__main__':
  states_to_create = 10
  games_created = 0
  with open(f'../data/data_generated/data_row_classify_connect_four_game_{states_to_create}.txt', 'w') as row_classify_file, open(f'../data/data_generated/data_row_unbiased_classify_connect_four_game_{states_to_create}.txt', 'w') as unbiased_row_classify_file, open(f'../data/data_generated/data_win_classify_connect_four_game_{states_to_create}.txt', 'w') as win_classify_file:
    # file header
    row_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
    win_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
      
    bot = Player('Bot', 'B')
    opposite = Player('Opposite', 'O')

    # states
    all_states = list()
    states_per_player = dict()
    states_per_column = dict()

    # initialise dicts to not check if in dict
    states_per_player[bot] = []
    states_per_player[opposite] = []
    for i in range(7):
      states_per_column[i] = []

    while (len(min(list(states_per_column.values()), key=len)) <= states_to_create):
      connect_four = ConnectFour(bot, opposite)

      while True:
        current_player = connect_four.current_player
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if connect_four.is_draw():
          # write all states for opposite
          for state in all_states:
            win_classify_file.write(f'{state};{0.5}\n')
          break

        cls()
        connect_four.board.print_with_colors(bot.signature, opposite.signature)
        while True:
          try:
            for column in states_per_column:
              print(f'States per column {column}: {len(states_per_column[column])}')
            print(f'Player: {current_player.name}, select column ( 1 - 7 )?')
            column_to_play = int(readchar.readkey()) - 1
            if (column_to_play > 6):
              raise Exception("Not a valid column")
            break
          except:
            print('Not a valid number, try again')
        # if (current_player is bot):
        # else:
        #   column_to_play = choice(connect_four.board.get_possible_columns())
          
        connect_four.move(column_to_play)

        # setup a dict of states_per_player per player, since we only need the states_per_player from the winning player
        state_after_player_move = StateAfterMove(copy(connect_four.board), current_player, column_to_play, connect_four.has_won())

        # for opposite
        all_states.append(state_after_player_move)

        # for bot
        states_per_player[current_player].append(state_after_player_move)
        
        if (current_player is bot):
          states_per_column[column_to_play].append(state_after_player_move)

        won_player = connect_four.has_won()
        if (won_player is not None):
          if (won_player is bot):
            games_created += 1
          break

      if games_created % 1000 is 0:
        print(f'progress: {games_created}/{states_to_create}.')
    
    # TODO: add to state which player has won
    for state in all_states:
      win_classify_file.write(f'{state};\n')

    for player in states_per_player:
      for state in states_per_player[player]:
          row_classify_file.write(f'{state};\n')
        
    minimum_amount_of_states = len(min(list(states_per_column.values()), key=len))
    column_states_unbiased = []
    for column in states_per_column:
      shuffle(states_per_column[column])
      for state in states_per_column[column][:minimum_amount_of_states]:
          column_states_unbiased.append(state)

    shuffle(column_states_unbiased)
    for state in column_states_unbiased:
      unbiased_row_classify_file.write(f'{state};\n')