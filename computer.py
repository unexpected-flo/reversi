import rules
from random import randint


class RandomAi:
    def __init__(self, color):
        self.color = color

    def play(self, board):
        pot_moves = list(rules.find_all_moves(board, self.color))
        selected_move = randint(0, len(pot_moves)-1)
        return pot_moves[selected_move]

class Minmax:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def evaluate_position(self, board):
        scores = {self.color: 0, "opponent": 0}
        for line in board.tiles:
            for tile in line:
                if tile is not None:
                    if tile == self.color:
                        scores[self.color] += 1
                    else:
                        scores["opponent"] += 1
        return scores[self.color] - scores["opponent"]

    def play(self, board):

        return




ai_types = {"random": RandomAi}
