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
  hypothesis_testing(list(correctness_per_player_data["Blocking moves"][:20]), list(correctness_per_player_data["Blocking moves"][20:]))

  plot = sns.boxplot(x="Type", y="Won against random", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Won against random (out of 100)")
  plot.figure.savefig(f"../statistics/images/analysis-won-against-random.png")
  plot.figure.clf()
  hypothesis_testing(list(correctness_per_player_data["Won against random"][:20]), list(correctness_per_player_data["Won against random"][20:]))

  plot = sns.boxplot(x="Type", y="Won against opposite", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel="Won against opposite (out of 100)")
  plot.figure.savefig(f"../statistics/images/analysis-won-against-opposite.png")
  plot.figure.clf()
  hypothesis_testing(list(correctness_per_player_data["Won against opposite"][:20]), list(correctness_per_player_data["Won against opposite"][20:]))

  won_against_random = list(correctness_per_player_data['Won against random'])
  plot = sns.boxplot(x="Type", y="Average moves played random", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel=f"Average moves played against random [{min(won_against_random)},{max(won_against_random)}]")
  plot.figure.savefig(f"../statistics/images/analysis-average-moves-played-random.png")
  plot.figure.clf()

  won_against_opposite = list(correctness_per_player_data['Won against opposite'])
  plot = sns.boxplot(x="Type", y="Average moves played opposite", data=correctness_per_player_data)
  plot.set(xlabel="Classifier", ylabel=f"Average moves played against opposite [{min(won_against_opposite)},{max(won_against_opposite)}]")
  plot.figure.savefig(f"../statistics/images/analysis-average-moves-played-opposite.png")
  plot.figure.clf()