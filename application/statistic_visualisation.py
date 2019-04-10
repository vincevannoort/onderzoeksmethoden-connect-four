from connect_four import ConnectFour, Board, Player
from copy import copy, deepcopy
import numpy as np
import pandas as pd
import pickle
from statsmodels.stats import weightstats as stests
from scipy import stats
import random
import math
import keras

from statistic_hypothesis_testing_ttest import hypothesis_testing 

import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.style as style

if __name__ == '__main__':
  with open(f'../statistics/dataframes/analysis_20.pickle', 'rb') as dataframe_file:
    correctness_per_player_data = pickle.load(dataframe_file)
  correctness_per_player_data = correctness_per_player_data.replace('model_jort', 'Win/Lose classifier')
  correctness_per_player_data = correctness_per_player_data.replace('model_vince', 'Column choice classifier')

  # colors
  sns.set_palette(["#63b7ff", "#00844a", "#e0e000"])
  # size (resolution)
  style.use('seaborn-poster')

  plot = sns.barplot(x="Player", y="Winning moves", palette=["#63b7ff"] * 10 + ["#00844a"] * 10, data=pd.concat([correctness_per_player_data[:10], correctness_per_player_data[20:30]]))
  plot.set(xlabel="Classifier", ylabel="Correct winning moves (out of 1000) per player")
  plot.figure.savefig(f"../statistics/images/analysis-winning-moves-per-player.png")
  plot.figure.clf()

  plot = sns.boxplot(x="Type", y="Winning moves", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Correct winning moves (out of 1000)")
  plot.figure.savefig(f"../statistics/images/analysis-winning-moves.png")
  plot.figure.clf()
  hypothesis_testing(list(correctness_per_player_data["Winning moves"][:20]), list(correctness_per_player_data["Winning moves"][20:]))

  plot = sns.boxplot(x="Type", y="Blocking moves", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Correct blocking moves (out of 1000)")
  plot.figure.savefig(f"../statistics/images/analysis-blocking-moves.png")
  plot.figure.clf()
  # print(list(correctness_per_player_data["Blocking moves"][:20]))
  # print(list(correctness_per_player_data["Blocking moves"][20:]))
  hypothesis_testing(list(correctness_per_player_data["Blocking moves"][:20]), list(correctness_per_player_data["Blocking moves"][20:]))

  plot = sns.boxplot(x="Type", y="Won against random", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Won against random (out of 1000)")
  plot.figure.savefig(f"../statistics/images/analysis-won-against-random.png")
  plot.figure.clf()
  hypothesis_testing(list(correctness_per_player_data["Won against random"][:20]), list(correctness_per_player_data["Won against random"][20:]))

  plot = sns.boxplot(x="Type", y="Draw against random", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Draw against random (out of 1000)")
  plot.figure.savefig(f"../statistics/images/analysis-draw-against-random.png")
  plot.figure.clf()

  plot = sns.boxplot(x="Type", y="Won against opposite", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Won against opposite (out of 100)")
  plot.figure.savefig(f"../statistics/images/analysis-won-against-opposite.png")
  plot.figure.clf()
  hypothesis_testing(list(correctness_per_player_data["Won against opposite"][:20]), list(correctness_per_player_data["Won against opposite"][20:]))

  plot = sns.boxplot(x="Type", y="Draw against opposite", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Draw against opposite (out of 100)")
  plot.figure.savefig(f"../statistics/images/analysis-draw-against-opposite.png")
  plot.figure.clf()

  wins_in_one_turn = []
  wins_in_two_turns = []
  wins_in_three_turns = []
  wins_in_four_turns = []
  wins_in_five_turns = []
  wins_in_six_turns = []
  for index, row in correctness_per_player_data.iterrows():
    wins_in_one_turn.append(row['Steps win against random'][1])
    wins_in_two_turns.append(row['Steps win against random'][2])
    wins_in_three_turns.append(row['Steps win against random'][3])
    wins_in_four_turns.append(row['Steps win against random'][4])
    wins_in_five_turns.append(row['Steps win against random'][5])
    wins_in_six_turns.append(row['Steps win against random'][6])

  correctness_per_player_data['t_one'] = wins_in_one_turn
  correctness_per_player_data['t_two'] = wins_in_two_turns
  correctness_per_player_data['t_three'] = wins_in_three_turns
  correctness_per_player_data['t_four'] = wins_in_four_turns
  correctness_per_player_data['t_fiv'] = wins_in_five_turns
  correctness_per_player_data['t_six'] = wins_in_six_turns
  print(correctness_per_player_data)

  plot = sns.boxplot(x="Type", y="t_one", data=correctness_per_player_data)
  plot = sns.boxplot(x="Type", y="t_two", data=correctness_per_player_data)
  plot = sns.boxplot(x="Type", y="t_three", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Only took 1 turn")
  plot.figure.savefig(f"../statistics/images/analysis-turns-against-random.png")
  plot.figure.clf()

  # plot = sns.factorplot('t_', hue='Type', y='c', data=correctness_per_player_data, kind='box')
  # plot.set(xlabel="Classifier", ylabel="Draw against opposite (out of 100)")
  # plot.figure.savefig(f"../statistics/images/analysis-turns_against_random.png")
  # plot.figure.clf()
  # melted_correctness_per_player_data = pd.melt(correctness_per_player_data, 'Type', var_name='t_', value_name='turns')
  # print(melted_correctness_per_player_data)
  # print(correctness_per_player_data['Steps win against random'])
  # print(correctness_per_player_data['Steps win against opposite'])