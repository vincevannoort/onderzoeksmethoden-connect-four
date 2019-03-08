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

    return f'{board_representation};{self.player.signature};{self.column_played};{self.game_won}\n'

if __name__ == '__main__':
  amount_to_create = 1
  games_created = 0
  with open(f'../data/data_generated/connect-four-game-{amount_to_create}.txt', 'w') as file:
    vince = Player('Vince', 'A')
    jort = Player('Jort', 'B')
    while games_created < amount_to_create:
      connect_four = ConnectFour(vince, jort)
      states = dict()
      while True:
        current_player = connect_four.current_player
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if connect_four.is_draw():
          break

        column_to_play = choice(connect_four.board.get_possible_columns())
        connect_four.move(column_to_play)
        print(current_player)
        print(connect_four.board)

        # setup a dict of states per player, since we only need the states from the winning player
        state_after_player_move = StateAfterMove(copy(connect_four.board), current_player, column_to_play, connect_four.has_won())
        if current_player in states:
          states[current_player].append(state_after_player_move)
        else:
          states[current_player] = [state_after_player_move]

        
        if (connect_four.has_won() is jort):
          break

        if (connect_four.has_won() is vince):
          games_created += 1
          for state in states[vince]:
            file.write(f'{state}')
          break

      if games_created % 1000 is 0:
        print(f'progress: {games_created}/{amount_to_create}.')