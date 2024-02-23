"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    player = None

    for row in board:
        for column in row:
            if column == O:
                count_o += 1
            elif column == X:
                count_x += 1
    
    if count_x > count_o:
        player = O
    elif count_x == count_o:
        player = X
    
    return player

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = []
    i = -1
    j = -1
    for row in board:
        i += 1
        j = -1
        for target in row:
            j += 1
            if target == None:
                available_actions.append((i,j))
    return available_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    state = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    state[i][j] = player(state)
    return state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = [] # rows, columns, and diagonals
    columns = list(zip(board[0], board[1], board[2])) # rotate board
    diagonal = [board[i][i] for i in range(len(board))]
    other_diagonal = [board[i][len(board) - 1 - i] for i in range(len(board))]

    # update lines
    for row in board:
        lines.append(row)

    for column in columns:
        lines.append(column)

    lines.append(diagonal)
    lines.append(other_diagonal)

    # check rows and return
    for line in lines:
        if len(set(line)) == 1:
            return line[0]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for rows in board:
        for column in rows:
            if column == None:
                return False
    
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v,min_value(result(board,action)))
    return v

def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
    return v

def minimax(board):
    if terminal(board):
        return None

    points = []
    
    for action in actions(board):
        if player(board) == X:
            points.append([min_value(result(board,action)),action])
            points = sorted(points, key=lambda x: x[0], reverse=True)
        elif player(board) == O:
            points.append([max_value(result(board,action)),action])
            points = sorted(points, key=lambda x: x[0])

    return points[0][1]