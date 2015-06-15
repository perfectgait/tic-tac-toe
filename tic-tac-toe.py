"""
Monte Carlo Tic-Tac-Toe Player
"""

__author__ = "Matt Rathbun"
__email__ = "mrathbun80@gmail.com"
__version__ = "1.0"

import random
import poc_simpletest
# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
NTRIALS = 1          # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0    # Score for squares played by the other player

def mc_trial(board, player):
    """
    Take a current board and the next player to move.  Then play a game starting with the given player by making random
    moves, alternating between players.
    """
    while True:
        empty_squares = board.get_empty_squares()

        if len(empty_squares) == 0:
            break

        empty_square = random.choice(empty_squares)

        board.move(empty_square[0], empty_square[1], player)

        if player == provided.PLAYERO:
            player = provided.PLAYERX
        else:
            player = provided.PLAYERO

def mc_update_scores(scores, board, player):
    """
    Update scores by adding the scores for a specified board
    """
    winning_player = board.check_win()
    dimension = board.get_dim()

    if winning_player is None or winning_player == provided.DRAW:
        return

    if winning_player != player:
        score_current = SCORE_CURRENT * -1
        score_other = SCORE_OTHER
    else:
        score_current = SCORE_CURRENT
        score_other = SCORE_OTHER * -1

    for row in range(0, dimension):
        for col in range(0, dimension):
            if board.square(row, col) == player:
                scores[row][col] += score_current
            else:
                scores[row][col] += score_other

def get_best_move(board, scores):
    """
    Get the best move for a board and a list of scores
    """
    empty_squares = board.get_empty_squares()
    best_score = 0
    best_square = None

    if len(empty_squares) <= 0:
        return None

    for empty_square in empty_squares:
        if scores[empty_square[0]][empty_square[1]] > best_score:
            best_score = scores[empty_square[0]][empty_square[1]]
            best_square = empty_square

    return best_square

def test_mc_trial():
    """
    Tests for mc_trial
    """
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(3)

    mc_trial(board, provided.PLAYERX)

    # print board

    # for row in board:
    #     for col in row:
    #         # @TODO Figure out how to make the suite honor 2 or 3
    #         suite.run_test(col, col)
    #
    # suite.report_results()

def test_mc_update_scores():
    """
    Tests for mc_update_scores
    """
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(3)
    scores = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    board = provided.TTTBoard(3)
    scores = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    board.move(0, 0, provided.PLAYERO)
    board.move(0, 1, provided.PLAYERX)
    board.move(0, 2, provided.PLAYERO)
    board.move(1, 0, provided.PLAYERX)
    board.move(1, 1, provided.PLAYERO)
    board.move(1, 2, provided.PLAYERX)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERX)
    board.move(2, 2, provided.PLAYERO)

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[1, -1, 1], [-1, 1, -1], [1, -1, 1]])

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[2, -2, 2], [-2, 2, -2], [2, -2, 2]])

    board = provided.TTTBoard(3)

    board.move(0, 0, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERO)
    board.move(0, 2, provided.PLAYERX)
    board.move(1, 0, provided.PLAYERO)
    board.move(1, 1, provided.PLAYERX)
    board.move(1, 2, provided.PLAYERO)
    board.move(2, 0, provided.PLAYERX)
    board.move(2, 1, provided.PLAYERO)
    board.move(2, 2, provided.PLAYERX)

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[3, -3, 3], [-3, 3, -3], [3, -3, 3]])

    board = provided.TTTBoard(3)

    board.move(0, 0, provided.PLAYERO)
    board.move(0, 1, provided.PLAYERO)
    board.move(0, 2, provided.PLAYERX)
    board.move(1, 0, provided.PLAYERO)
    board.move(1, 1, provided.PLAYERX)
    board.move(1, 2, provided.PLAYERO)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERO)
    board.move(2, 2, provided.PLAYERX)

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[4, -2, 2], [-2, 2, -2], [4, -2, 2]])

    suite.report_results()

def test_get_best_move():
    """
    Tests for get_best_move
    """
    suite = poc_simpletest.TestSuite()

    suite.report_results()


test_mc_trial()
test_mc_update_scores()
test_get_best_move()




# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
