from connect_four import ConnectFour, Board, Player
from copy import copy, deepcopy
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
from statsmodels.stats import weightstats as stests
from scipy import stats
import random
import math
import keras

if __name__ == '__main__':
  with open(f'../statistics/dataframes/analysis.pickle', 'rb') as dataframe_file:
    correctness_per_player_data = pickle.load(dataframe_file)

  print(correctness_per_player_data)
  print(list(correctness_per_player_data['Winning moves']))
  print(stats.tvar(list(correctness_per_player_data['Winning moves'])))
  print(math.sqrt(stats.tvar(list(correctness_per_player_data['Winning moves']))))

  # plot for winning per model - 100 bars
  plot_winning = sns.barplot(x="Player", y="Winning moves", data=correctness_per_player_data, ci='sd')
  plot_winning.set(ylim=(0, 10000))
  plot_winning.figure.savefig(f"../statistics/images/analysis-winning-moves.png")

  # plot for winning per classifier - 2 bars

  # plot for blocking per model - 100 bars
  plot_blocking = sns.barplot(x="Player", y="Blocking moves", data=correctness_per_player_data)
  plot_blocking.set(ylim=(0, 10000))
  plot_blocking.figure.savefig(f"../statistics/images/analysis-blocking-moves.png")  

  # plot for blocking per classifier - 2 bars