import rules
from random import randint
from copy import deepcopy


class RandomAi:
    def __init__(self, color):
        self.color = color

    def play(self, board):
        pot_moves = list(rules.find_all_moves(board, self.color))
        selected_move = randint(0, len(pot_moves)-1)
        return pot_moves[selected_move]


class Minimax:
    def __init__(self, color, opponent, depth=3):
        self.color = color
        self.depth = depth
        self.opponent = opponent

    def evaluate_position(self, board):
        scores = {self.color: 0, self.opponent: 0}
        for line in board.tiles:
            for tile in line:
                if tile is not None:
                    scores[tile] += 1
        for tile in [board.tiles[0][0], board.tiles[board.size-1][board.size-1],
                     board.tiles[0][board.size-1], board.tiles[board.size-1][0]]:
            if tile is not None:
                scores[tile] += 3
        for i in range(board.size-1):
            for tile in [board.tiles[0][i], board.tiles[i][0], board.tiles[board.size-1][i], board.tiles[i][board.size-1]]:
                if tile is not None:
                    scores[tile] += 2

        return scores[self.color] - scores[self.opponent]

    def minimax(self, board, player, depth, alpha, beta):
        best_plays = []
        if rules.check_game_over(board, self.color, self.opponent) or depth == 0:
            return self.evaluate_position(board), best_plays
        if player == self.color:
            score = float("-inf")
            for play in rules.find_all_moves(board, player):
                tmp_brd = deepcopy(board)
                rules.execute_move(*play, tmp_brd, self.color)
                tmp_score = self.minimax(tmp_brd, self.opponent, depth-1, alpha, beta)[0]
                if tmp_score >= score:
                    score = tmp_score
                    if depth == self.depth:
                        best_plays.append(play)
                alpha = max(alpha, score)
                if score >= beta:
                    break
            return score, best_plays
        elif player == self.opponent:
            score = float("inf")
            for play in rules.find_all_moves(board, player):
                tmp_brd = deepcopy(board)
                rules.execute_move(*play, tmp_brd, self.opponent)
                score = min(score, self.minimax(tmp_brd, self.color, depth-1, alpha, beta)[0])
                beta = min(beta, score)
                if score <= alpha:
                    break
            return score, best_plays

    def play(self, board):
        _, plays = self.minimax(board, self.color, self.depth, float("-inf"), float("inf"))
        choice = randint(0, len(plays)-1)
        return plays[choice]


class MCTS:
    def __init__(self):
        pass

ai_types = {"random": RandomAi, "minimax": Minimax}
# Minimax (v1) depth 3 vs random {'Black': 624, 'White': 344, 'Draw': 32}
# Minimax (v2) depth 3 vs random {'Black': 771, 'White': 195, 'Draw': 34}
# random vs random {'Black': 463, 'White': 500, 'Draw': 37}