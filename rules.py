def find_all_moves(board, active_player):
    """returns a list of tuples for coordinates where the active player can place a pawn"""
    legal_moves = []
    for l, line in enumerate(board.tiles):
        for c, tile in enumerate(line):
            if tile is None:
                for horizontal in [-1, 0, 1]:
                    for vertical in [-1, 0, 1]:
                        if test_direction_legality(l, c, horizontal, vertical, board, active_player):
                            legal_moves.append((l, c))

    return set(legal_moves)


def test_direction_legality(line, column, horizontal_direction, vertical_direction, board, active_player):
    """finds if there is a valid move to be played from the empty tile located at board[line][column]"""
    flag = False
    while 0 <= line+vertical_direction < board.size and 0 <= column+horizontal_direction < board.size:
        line += vertical_direction
        column += horizontal_direction
        if board.tiles[line][column] is not active_player and board.tiles[line][column] is not None:
            flag = True
        elif board.tiles[line][column] is active_player and flag:
            return True
        else:
            return False

    return False


def execute_move(line, column, board, active_player):
    """update the board after move by active player"""
    board.tiles[line][column] = active_player
    for horizontal in [-1, 0, 1]:
        for vertical in [-1, 0, 1]:
            if (horizontal, vertical) != (0, 0):
                capture_direction(line, column, horizontal, vertical, board, active_player)


def capture_direction(line, column, horizontal_direction, vertical_direction, board, active_player):
    to_capture = []
    flag = False
    while 0 <= line+vertical_direction < board.size and 0 <= column+horizontal_direction < board.size:
        line += vertical_direction
        column += horizontal_direction
        if board.tiles[line][column] is not active_player and board.tiles[line][column] is not None:
            flag = True
            to_capture.append((line, column))
        elif board.tiles[line][column] is active_player and flag:
            for l, c in to_capture:
                board.tiles[l][c] = active_player
            return
        else:
            return

def check_game_over(board, player1, player2):
        gameover = True
        for line in board.tiles:
            for tile in line:
                if tile is None:
                    gameover = False
        if len(find_all_moves(board, player1)) == 0 and\
                len(find_all_moves(board, player2)) == 0:
            gameover = True
        return gameover


