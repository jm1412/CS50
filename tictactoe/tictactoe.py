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
    else:
        return 0


def minimax_working(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    me = player(board)
    available_actions = actions(board)

    # simulate my moves and adversary moves
    for action in available_actions:
        simulated_board = copy.deepcopy(board)
        board_1 = result(simulated_board, action)
        if me == winner(board_1):
            return action

        # Check every enemy actions
        enemy = player(board_1)
        enemy_actions = actions(board_1)
        
        enemy_wins = False
        for enemy_action in enemy_actions:
            simulated_board2 = copy.deepcopy(board_1)
            board_2 = result(simulated_board2, enemy_action)

            #logic here
            if winner(board_2) == enemy:
                enemy_wins = True
        
        if enemy_wins == False:
            return action
        
    return action

def minimax(board):
    if terminal(board): return None
    me = player(board)
    points = []
    available_actions = actions(board)
    for action in available_actions:
        sim = copy.deepcopy(board)
        sim = result(sim,action)
        points.append([minimaxer(sim),action])


    if me == X:
        points = sorted(points, key=lambda x: (x[0], x[1][0]), reverse=True)    
    else:
        points = sorted(points, key=lambda x: (x[0], x[1][0]))
    print(points)    
    return points[0][1]

def minimaxer(board):
    points = utility(board)
    sim = copy.deepcopy(board)
    available_actions = actions(sim)
    for action in available_actions:
        sim = result(sim,action)
        points += utility(sim)
        return points + minimaxer(sim)
    return 0


def minimax_depth(board):
    simulated_board = copy.deepcopy(board)
    available_actions = actions(simulated_board)
    me = player(simulated_board)

    for action in available_actions:
        simulated_board = result(simulated_board, action)
        if winner(simulated_board) == me:
            return action
        
        return minimax_depth(simulated_board)

def minimax_dfs(board):
    
    me = player(board)
    my_actions_1 = actions(board)
    priority_action = None

    for my_action_1 in my_actions_1:
        simulated_board_1 = copy.deepcopy(board)
        simulated_board_1 = result(simulated_board_1, my_action_1)    
        if winner(simulated_board_1) == me:
            return my_action_1
        enemy = player(simulated_board_1)
        enemy_actions_1 = actions(simulated_board_1)

        for enemy_action_1 in enemy_actions_1:
            simulated_board_2 = copy.deepcopy(simulated_board_1)
            simulated_board_2 = result(simulated_board_2, enemy_action_1)
            if winner(simulated_board_2) == enemy:
                priority_action = enemy_action_1

            me = player(simulated_board_2)
            my_actions_2 = actions(simulated_board_2)

            if priority_action == None:
                for my_action_2 in my_actions_2:
                    simulated_board_3 = copy.deepcopy(simulated_board_2)
                    simulated_board_3 = result(simulated_board_2, my_action_2)
                    if winner(simulated_board_3) == me:
                        priority_action = my_action_2

    # this being a nested for-loop is a sign that I can simplify this
    if priority_action:
        return priority_action
    else:
        return my_action_1