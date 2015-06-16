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
NTRIALS = 1000       # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0    # Score for squares played by the other player

def mc_trial(board, player):
    """
    Take a current board and the next player to move.  Then play a game starting with the given player by making random
    moves, alternating between players.
    """
    while True:
        empty_squares = board.get_empty_squares()

        if len(empty_squares) == 0 or board.check_win() is not None:
            break

        empty_square = random.choice(empty_squares)

        board.move(empty_square[0], empty_square[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Update scores by adding the scores for a specified board
    """
    winning_player = board.check_win()
    dimension = board.get_dim()
    opponent = provided.switch_player(player)

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
            elif board.square(row, col) == opponent:
                scores[row][col] += score_other

def get_best_move(board, scores):
    """
    Get the best move for a board and a list of scores
    """
    empty_squares = board.get_empty_squares()
    best_score = None
    choices = []

    if len(empty_squares) <= 0:
        return None

    for empty_square in empty_squares:
        if best_score is None or scores[empty_square[0]][empty_square[1]] > best_score:
            best_score = scores[empty_square[0]][empty_square[1]]
            choices = [empty_square]
        elif scores[empty_square[0]][empty_square[1]] == best_score:
            choices.append(empty_square)

    if len(choices) > 0:
        return random.choice(choices)

def mc_move(board, player, trials):
    """
    Use a Monte Carlo simulation to return a move for the specified player
    """
    if trials > 0:
        scores = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]

        for dummy_i in range(trials):
            cloned_board = board.clone()
            mc_trial(cloned_board, player)
            mc_update_scores(scores, cloned_board, player)

        best_move = get_best_move(board, scores)

        if best_move is not None:
            return best_move

def test_mc_trial():
    """
    Tests for mc_trial
    """
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(3)

    mc_trial(board, provided.PLAYERX)

    if board.check_win() is not None:
        suite.run_test(True, True)
    else:
        suite.run_test(False, True)

    board = provided.TTTBoard(5)

    mc_trial(board, provided.PLAYERX)

    if board.check_win() is not None:
        suite.run_test(True, True)
    else:
        suite.run_test(False, True)

    suite.report_results()

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

    board = provided.TTTBoard(3)

    board.move(0, 0, provided.PLAYERO)
    board.move(0, 1, provided.PLAYERO)
    board.move(0, 2, provided.PLAYERX)
    board.move(1, 0, provided.PLAYERO)
    board.move(1, 1, provided.PLAYERX)
    board.move(1, 2, provided.PLAYERO)
    board.move(2, 0, provided.PLAYERO)

    mc_update_scores(scores, board, provided.PLAYERX)

    suite.run_test(scores, [[5, -1, 1], [-1, 1, -1], [5, -2, 2]])

    suite.report_results()

def test_get_best_move():
    """
    Tests for get_best_move
    """
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(3)

    board.move(0, 0, provided.PLAYERO)
    board.move(0, 1, provided.PLAYERX)
    board.move(0, 2, provided.PLAYERO)
    board.move(1, 0, provided.PLAYERX)
    board.move(1, 1, provided.PLAYERO)
    board.move(1, 2, provided.PLAYERX)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERX)

    scores = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    suite.run_test(get_best_move(board, scores), (2, 2))

    board = provided.TTTBoard(3)

    board.move(0, 0, provided.PLAYERO)
    board.move(0, 1, provided.PLAYERO)
    board.move(0, 2, provided.PLAYERX)
    board.move(1, 0, provided.PLAYERO)
    board.move(1, 1, provided.PLAYERX)
    board.move(1, 2, provided.PLAYERO)

    scores = [
        [1, 1, -1],
        [1, -1, 1],
        [2, 3, 3]
    ]

    best_move = get_best_move(board, scores)

    if best_move == (2, 1) or best_move == (2, 2):
        suite.run_test(1, 1)
    else:
        suite.run_test(0, 1)

    suite.report_results()

def test_mc_move():
    """
    Tests for mc_move
    """
    suite = poc_simpletest.TestSuite()

    board = provided.TTTBoard(
        3,
        False,
        [
            [provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
            [provided.EMPTY, provided.PLAYERX, provided.PLAYERX],
            [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]
        ]
    )

    move = mc_move(board, provided.PLAYERO, NTRIALS)

    suite.run_test(move, (2, 1))

    suite.report_results()


test_mc_trial()
test_mc_update_scores()
test_get_best_move()
test_mc_move()

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
