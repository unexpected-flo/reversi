import board as brd
import rules
import interface
import computer


class Player:
    def __init__(self, color, human=True, ai_selected=None, ai_args=None):
        self.color = color
        self.human = human
        if not human:
            self.cpu = computer.ai_types[ai_selected](*ai_args)

    def select_move(self, board, window):
        if self.human:
            return Game.get_player_input(game, window)
        else:
            return self.cpu.play(board)


class Game:
    def __init__(self, players, user_interface="cli"):
        self.game_over = False
        self.players = players
        self.active_player = players[0]
        self.board = self.init_board(8)
        self.ui = user_interface

    def init_board(self, size):
        board = brd.Board(size)
        board.tiles[3][3] = self.players[1].color
        board.tiles[4][4] = self.players[1].color
        board.tiles[3][4] = self.players[0].color
        board.tiles[4][3] = self.players[0].color
        return board

    def change_active_player(self):
        if self.active_player == self.players[0]:
            self.active_player = self.players[1]
        elif self.active_player == self.players[1]:
            self.active_player = self.players[0]

    def turn(self, window=None):
        potential_moves = rules.find_all_moves(self.board, self.active_player.color)
        if len(potential_moves) == 0:
            self.change_active_player()
            return
        line, column = self.active_player.select_move(self.board, window)
        if (line, column) in potential_moves:
            rules.execute_move(line, column, self.board, self.active_player.color)
            self.change_active_player()

    def get_player_input(self, window):
        if self.ui == "cli":
            print("{} turns".format(self.active_player.color))
            print("Input line, column coordinates to place pawn")
            line, column = [int(x) for x in input().split(sep=",")]
            return line, column
        if self.ui == "gui":
            line, column = interface.get_event(window)
            return line, column

    def find_winner(self, board):
        score = {self.players[0].color: 0, self.players[1].color: 0}
        for line in board.tiles:
            for tile in line:
                if tile is not None:
                    score[tile] += 1
        if score[self.players[0].color] > score[self.players[1].color]:
            return self.players[0].color, score[self.players[0].color], score[self.players[1].color]
        elif score[self.players[1].color] > score[self.players[0].color]:
            return self.players[1].color, score[self.players[1].color], score[self.players[0].color]
        else:
            return None

    def play(self):
        window = None
        if self.ui == "gui":
            window = interface.create_window("Reversi", self.board.size, self.board)

        while not self.game_over:
            if self.ui == "cli":
                interface.draw_cli_board(self.board)
            elif self.ui == "gui":
                interface.redraw_board(window, self.board)
            else:
                pass
            self.turn(window)
            self.game_over = rules.check_game_over(self.board, self.players[0].color, self.players[1].color)
        winner = self.find_winner(self.board)
        if winner is None:
            print("Draw")
            return "Draw"
        else:
            print("winner is {}, {} to {}".format(*winner))
            return winner[0]


if __name__ == "__main__":
    player_1 = Player("Black", False, "minimax", ["Black", "White", 3])
    player_2 = Player("White", False, "random", ["White"])

    # player_1 = Player("Black", True)
    # player_2 = Player("White", True)

    game = Game([player_1, player_2], user_interface="gui")
    game.play()
