# reference: https://raw.githubusercontent.com/erikackermann/Connect-Four/a627bf7615c4d71f05ea1496be629b2a46225efc/minimax.py

import random
from copy import deepcopy
from connect_four import *
import numpy as np
import readchar
from random import choice

class Minimax:
    """ Minimax object that takes a current connect four board state
    """
    def __init__(self, board):
        # deepcopy the board to self.board
        self.board = board
            
    def best_move(self, depth, board, current_player, opposite_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        legal_moves = {}
        for column in range(7):
            if board.get_hole(column, 0) is 0:
                temp = deepcopy(board)
                temp.set_column(column, current_player)
                legal_moves[column] = -self.search(depth-1, temp, opposite_player, current_player)
        
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha > best_alpha:
                best_alpha = alpha
                best_move = [move]
            elif alpha == best_alpha and best_alpha is not -99999999:
              if (best_move is not None):
                best_move.append(move)
        
        return best_move, best_alpha
        
    def search(self, depth, board, current_player, opposite_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        legal_boards = []
        for column in range(7):
            if board.get_hole(column, 0) is 0:
                temp = deepcopy(board)
                temp.set_column(column, current_player)
                legal_boards.append(temp)
        
        if depth == 0 or len(legal_boards) == 0 or self.game_is_over(board, current_player, opposite_player):
            return self.value(board, current_player, opposite_player)

        alpha = -99999999

        for legal_board in legal_boards:
            alpha = max(alpha, -self.search(depth-1, legal_board, opposite_player, current_player))
        return alpha
    
    def game_is_over(self, board, current_player, opposite_player):
        if self.check_for_streak(board, current_player, 4) >= 1:
            return True
        elif self.check_for_streak(board, opposite_player, 4) >= 1:
            return True
        else:
            return False

    def value(self, board, current_player, opposite_player):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        my_fours = self.check_for_streak(board, current_player, 4)
        my_threes = self.check_for_streak(board, current_player, 3)
        my_twos = self.check_for_streak(board, current_player, 2)
        opp_fours = self.check_for_streak(board, opposite_player, 4)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
            
    def check_for_streak(self, board, current_player, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if board.get_hole(j, i) == current_player.signature:
                    count += self.vertical_streak(i, j, board, streak)
                    count += self.horizontal_streak(i, j, board, streak)
                    count += self.diagonal_check(i, j, board, streak)

        return count
            
    def vertical_streak(self, row, col, board, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if board.get_hole(col, i) == board.get_hole(col, row):
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def horizontal_streak(self, row, col, board, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if board.get_hole(j, row) == board.get_hole(col, row):
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def diagonal_check(self, row, col, board, streak):
        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif board.get_hole(j, i) == board.get_hole(col, row):
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif board.get_hole(j, i) ==  board.get_hole(col, row):
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total


if __name__ == "__main__":
    first_player = Player("Vince", 'V')
    second_player = Player("Bot", 'B')
    connect_four = ConnectFour(first_player, second_player)
    connect_four.current_player = first_player
    connect_four.move(2) #
    connect_four.move(1)
    connect_four.move(2) #
    connect_four.move(1)
    connect_four.move(4) #
    connect_four.move(3)
    connect_four.move(3) #
    connect_four.move(6)
    connect_four.move(2) #
    connect_four.move(2)
    connect_four.move(3) #

    while True:
      connect_four.board.print_with_colors(first_player.signature, second_player.signature)
      if connect_four.current_player is first_player:
        while True:
          try:
            print(f'Player: {connect_four.current_player.name}, select column ( 1 - 7 )?')
            column = int(readchar.readkey()) - 1
            connect_four.move(column)
            break
          except:
            print('Not a valid number, try again')
      else:
        mini_max = Minimax(connect_four.board)
        (best_move, alpha) = mini_max.best_move(5, connect_four.board, second_player, first_player)
        connect_four.move(best_move)
