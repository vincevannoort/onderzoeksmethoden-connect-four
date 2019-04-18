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
import argparse

from statistic_hypothesis_testing_ttest import hypothesis_testing 

import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.style as style

class Visualizer:
  def __init__(self, args):
    with open(f"../statistics/dataframes/analysis_{args.name1}_{args.name2}_{args.amount}.pickle", 'rb') as dataframe_file:
      self.results_per_player_data = pickle.load(dataframe_file)
    # colors
    sns.set_palette(["#63b7ff", "#00844a", "#e0e000"])
    # size (resolution)
    style.use('seaborn-poster')
    # set args
    self.name1 = args.name1
    self.name2 = args.name2
    self.amount = int(args.amount)
    self.save_path = f"../statistics/images/analysis-{self.name1}-{self.name2}"
  
  def plot_winning_moves_per_player(self):
    plot = sns.barplot(
      x=self.results_per_player_data.index, 
      y="Winning moves", 
      palette=["#63b7ff"] * self.amount + ["#00844a"] * self.amount, 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel="Correct winning moves (out of 1000) per player"
    )
    plot.figure.savefig(f"{self.save_path}-winning-moves-per-player.png")
    plot.figure.clf()
  
  def plot_winning_moves(self):
    plot = sns.boxplot(
      x="Player", 
      y="Winning moves", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel="Correct winning moves (out of 1000)"
    )
    plot.figure.savefig(f"{self.save_path}-winning-moves.png")
    plot.figure.clf()
    print("Hypothesis Testing Winning Moves")
    hypothesis_testing(list(self.results_per_player_data["Winning moves"][:self.amount]), list(self.results_per_player_data["Winning moves"][self.amount:]))
  
  def plot_blocking_moves(self):
    plot = sns.boxplot(
      x="Player", 
      y="Blocking moves", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel="Correct blocking moves (out of 1000)"
    )
    plot.figure.savefig(f"{self.save_path}-blocking-moves.png")
    plot.figure.clf()
    hypothesis_testing(list(self.results_per_player_data["Blocking moves"][:self.amount]), list(self.results_per_player_data["Blocking moves"][self.amount:]))

  def plot_won_against_random(self):
    plot = sns.boxplot(
      x="Player", 
      y="Won against random", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel="Won against random (out of 100)"
    )
    plot.figure.savefig(f"{self.save_path}-won-against-random.png")
    plot.figure.clf()
    hypothesis_testing(list(self.results_per_player_data["Won against random"][:self.amount]), list(self.results_per_player_data["Won against random"][self.amount:]))

  def plot_won_against_opposite(self):
    plot = sns.boxplot(
      x="Player", 
      y="Won against opposite", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel="Won against opposite (out of 100)"
    )
    plot.figure.savefig(f"{self.save_path}-won-against-opposite.png")
    plot.figure.clf()
    hypothesis_testing(list(self.results_per_player_data["Won against opposite"][:self.amount]), list(self.results_per_player_data["Won against opposite"][self.amount:]))

  def plot_average_moves_against_random(self):
    won_against_random = list(self.results_per_player_data['Won against random'])
    plot = sns.boxplot(
      x="Player", 
      y="Average moves played random", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel=f"Average moves played against random [{min(won_against_random)},{max(won_against_random)}]"
    )
    plot.figure.savefig(f"{self.save_path}-average-moves-played-random.png")
    plot.figure.clf()
  
  def plot_average_moves_against_opposite(self):
    won_against_opposite = list(self.results_per_player_data['Won against opposite'])
    plot = sns.boxplot(
      x="Player", 
      y="Average moves played opposite", 
      data=self.results_per_player_data
    )
    plot.set(
      xlabel="Classifier", 
      ylabel=f"Average moves played against opposite [{min(won_against_opposite)},{max(won_against_opposite)}]"
    )
    plot.figure.savefig(f"{self.save_path}-average-moves-played-opposite.png")
    plot.figure.clf()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--name1", "-n1", help="name of model", type=str)
  parser.add_argument("--name2", "-n2", help="name of model", type=str)
  parser.add_argument("--amount", "-a", help="amount of models tested", type=int, default=20)
  args = parser.parse_args()

  visualizer = Visualizer(args)
  visualizer.plot_winning_moves_per_player()
  visualizer.plot_winning_moves()
  visualizer.plot_blocking_moves()
  visualizer.plot_won_against_random()
  visualizer.plot_won_against_opposite()
  visualizer.plot_average_moves_against_random()
  visualizer.plot_average_moves_against_opposite()