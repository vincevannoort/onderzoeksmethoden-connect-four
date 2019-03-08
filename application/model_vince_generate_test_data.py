from connect_four import ConnectFour, Board, Player
from random import choice
from copy import copy

class StateAfterMove:
  def __init__(self, board: Board, player: Player, column_played: int, game_won: bool):
    self.board = board
    self.player = player
    self.column_played = column_played
    self.game_won = game_won

  def __str__(self):
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
    for hole in self.board.holes:
      board_representation += hole_to_array(hole, self.player)

    return f'{board_representation};{self.player.signature};{self.column_played};{True if self.game_won else False}'

if __name__ == '__main__':
  amount_to_create = 10000
  games_created = 0
  with open(f'../data/data_generated/data_row_classify_connect_four_game_{amount_to_create}.txt', 'w') as row_classify_file, open(f'../data/data_generated/data_win_classify_connect_four_game_{amount_to_create}.txt', 'w') as win_classify_file:
    # file header
    row_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
    win_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
      
    bot = Player('Bot', 'A')
    opposite = Player('Opposite', 'B')
    while (games_created < amount_to_create):
      connect_four = ConnectFour(bot, opposite)
      states_per_player = dict()
      all_states = list()
      while True:
        current_player = connect_four.current_player
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if connect_four.is_draw():
          # write all states for opposite
          for state in all_states:
            win_classify_file.write(f'{state};{0.5}\n')
          break

        column_to_play = choice(connect_four.board.get_possible_columns())
        connect_four.move(column_to_play)

        # setup a dict of states_per_player per player, since we only need the states_per_player from the winning player
        state_after_player_move = StateAfterMove(copy(connect_four.board), current_player, column_to_play, connect_four.has_won())

        # for opposite
        all_states.append(state_after_player_move)

        # for bot
        if current_player in states_per_player:
          states_per_player[current_player].append(state_after_player_move)
        else:
          states_per_player[current_player] = [state_after_player_move]

        
        won_player = connect_four.has_won()
        if (won_player is not None):

          # write all states for opposite
          for state in all_states:
            win_classify_file.write(f'{state};{1 if won_player is bot else 0}\n')

          # write only winning states for bot
          if (won_player is bot):
            games_created += 1
            for state in states_per_player[bot]:
              row_classify_file.write(f'{state};{1 if won_player is bot else 0}\n')
          break

      if games_created % 1000 is 0:
        print(f'progress: {games_created}/{amount_to_create}.')