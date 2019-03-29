# Personal files
from connect_four import ConnectFour, Board, Player
from tensorflow import keras

# Helper libraries
import numpy as np
import readchar
from minimax import Minimax
from random import choice
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

configuration = 'model_jort_vs_model_vince'
