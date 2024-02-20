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
        for target in row:
            j += 1
            if target == None:
                available_actions.append((i,j))

    return available_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    me = player(board)

    board[i][j] = me

    return board

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
    if winner(board) != None:
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
    elif terminal(board) == True:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    me = player(board)
    available_actions = actions(board)

    # simulate my moves and adversary moves
    simulated_board = copy.deepcopy(board)

    for action in available_actions:
        board_1 = result(simulated_board, action)
        if me == winner(board_1):
            return action

        enemy = player(board_1)
        enemy_actions = actions(board_1)
        
        for enemy_action in enemy_actions:
            board_2 = result(board_1, enemy_action)
            if winner(board_2) != enemy:
                print(f"board: {board}")
                print(f"simulated_board {simulated_board}")
                return action
    return action
