class Board:
    def __init__(self, size):
        self.size = size
        self.tiles = []
        for line in range(size):
            row = []
            for _ in range(size):
                row.append(None)
            self.tiles.append(row)


if __name__ == "__main__":
    board = Board(8)
    print(board.tiles)
    print(board.tiles)
    print(board.tiles[1][1] == board.tiles[2][1])


