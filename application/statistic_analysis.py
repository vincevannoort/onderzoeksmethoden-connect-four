from connect_four import ConnectFour, Board, Player
from copy import copy, deepcopy
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import keras
import argparse
from multiprocessing import Pool

class Analysis:
  def __init__(self, args):
    self.args = args
    self.random_player = Player("random", 'S', "random")
    self.players_one = [Player(
      args.name1, 
      'F',
      args.classifier1,
      self.load_model(i, args.winning1, args.blocking1, args.random_winning1, args.random_losing1, args.classifier1))
      for i in range(args.amount)
    ]
    self.players_two = [Player(
      args.name2, 
      'F',
      args.classifier2,
      self.load_model(i, args.winning2, args.blocking2, args.random_winning2, args.random_losing2, args.classifier2))
      for i in range(args.amount)
    ]
    self.player_one_opposite = deepcopy(self.players_one[0])
    self.player_one_opposite.signature = 'S'
    self.player_two_opposite = deepcopy(self.players_two[0]) 
    self.player_two_opposite.signature = 'S'
    self.players = self.players_one + self.players_two
    print("Done loading players")

    with open(f'../statistics/tests/random_make_winning_move_states_1000.txt', 'rb') as winning_move_states_file:
      self.winning_moves_states = pickle.load(winning_move_states_file)
    with open(f'../statistics/tests/random_make_blocking_move_states_1000.txt', 'rb') as blocking_move_states_file:
      self.blocking_move_states = pickle.load(blocking_move_states_file)
    with open(f'../statistics/tests/random_random_board_states_1000.txt', 'rb') as random_board_states_file:
      self.random_board_states = pickle.load(random_board_states_file)
    print("Done loading tests")

  def load_model(self, i, winning, blocking, random_winning, random_losing, classifier):
    if classifier == "winlose":
      return keras.models.load_model(f"../models/t{winning + blocking + random_winning + random_losing}_w{winning}_b{blocking}_rw{random_winning}_rl{random_losing}_model_{classifier}_{i}.h5")
    elif classifier == 'columnchoice':
      return keras.models.load_model(f"../models/t{winning + blocking + random_winning}_w{winning}_b{blocking}_rw{random_winning}_model_{classifier}_{i}.h5")
    else:
      raise Exception("Model could not be found.")

  def make_winning_moves(self, player: Player):
    correct_winning_moves = 0
    for(winning_state_connect_four, column) in self.winning_moves_states:
      connect_four = deepcopy(winning_state_connect_four)
      connect_four.first_player = player
      connect_four.current_player = player
      predicted_move = connect_four.get_move()
      if(predicted_move == column):
        correct_winning_moves += 1
    return correct_winning_moves

  def make_blocking_moves(self, player: Player):
    correct_blocking_moves = 0
    for(blocking_state_connect_four, column) in self.blocking_move_states:
      connect_four = deepcopy(blocking_state_connect_four)
      connect_four.first_player = player
      connect_four.current_player = player
      predicted_move = connect_four.get_move()
      if(predicted_move == column):
        correct_blocking_moves += 1
    return correct_blocking_moves

  def moves_played_against(self, player: Player, opposite: Player):
    total_moves_played = 0
    won_against = 0
    draw_against = 0
    for random_connect_four in self.random_board_states[:100]:
      connect_four = deepcopy(random_connect_four)
      connect_four.first_player = player
      connect_four.second_player = opposite
      moves_played = 0
      while not(connect_four.is_draw() or connect_four.has_won()):
        if connect_four.current_player is player:
          moves_played += 1
        connect_four.play_move()
      
        if(connect_four.has_won() is player):
          total_moves_played += moves_played
          won_against += 1 

        elif(connect_four.is_draw()):
          draw_against += 1
    return (total_moves_played, won_against, draw_against)

  def test_player(self, player: Player, index: int):
    print(f"Started for player: {index}")
    correct_winning_moves = self.make_winning_moves(player)
    correct_blocking_moves = self.make_blocking_moves(player)
    (total_moves_played_random, won_against_random, draw_against_random) = self.moves_played_against(player, self.random_player)
    opposite_player = self.player_two_opposite if player.name == args.name1 else self.player_one_opposite
    (total_moves_played_opposite, won_against_opposite, draw_against_opposite) = self.moves_played_against(player, opposite_player)

    return (
      player.name,
      player.type,
      correct_winning_moves,
      correct_blocking_moves,
      won_against_random,
      draw_against_random,
      total_moves_played_random,
      total_moves_played_random / won_against_random,
      won_against_opposite,
      draw_against_opposite,
      total_moves_played_opposite,
      total_moves_played_opposite / won_against_opposite
    )

  def testing(self):
    results_per_player = [self.test_player(player, index) for (index, player) in enumerate(self.players)]
    results_per_player_data = pd.DataFrame(results_per_player, columns = [
      'Player',
      'Type',
      'Winning moves', 
      'Blocking moves', 
      'Won against random', 
      'Draw against random',
      'Total moves played random',
      'Average moves played random',
      'Won against opposite', 
      'Draw against opposite', 
      'Total moves played opposite',
      'Average moves played opposite'
    ])

    print(results_per_player_data)
    with open(f'../statistics/dataframes/analysis_{args.name1}_{args.name2}_{args.amount}.pickle', 'wb') as dataframe_file:
      pickle.dump(results_per_player_data, dataframe_file)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning1", "-w1", help="amount of winning moves", type=int, default=75000)
  parser.add_argument("--blocking1", "-b1", help="amount of blocking moves", type=int, default=75000)
  parser.add_argument("--random_winning1", "-rw1", help="amount of random moves", type=int, default=0)
  parser.add_argument("--random_losing1", "-rl1", help="amount of random moves", type=int, default=0)
  parser.add_argument("--classifier1", "-c1", help="which classifier", type=str)
  parser.add_argument("--name1", "-n1", help="name of model", type=str)
  parser.add_argument("--winning2", "-w2", help="amount of winning moves", type=int, default=37500)
  parser.add_argument("--blocking2", "-b2", help="amount of blocking moves", type=int, default=37500)
  parser.add_argument("--random_winning2", "-rw2", help="amount of random moves", type=int, default=0)
  parser.add_argument("--random_losing2", "-rl2", help="amount of random moves", type=int, default=0)
  parser.add_argument("--classifier2", "-c2", help="which classifier", type=str)
  parser.add_argument("--name2", "-n2", help="name of model", type=str)
  parser.add_argument("--amount", "-a", help="amount of models", type=int, default=20)
  args = parser.parse_args()

  analysis = Analysis(args)
  analysis.testing()