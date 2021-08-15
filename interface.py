import string
import PySimpleGUI as sg

black_pawn = "./black_pawn.png"
white_pawn = "./white_pawn.png"
empty = "./blank.png"
images = {"White": white_pawn, "Black": black_pawn, None: empty}


def draw_cli_board(board):
    cli = {None: " ", "White": "W", "Black": "B"}
    for line in board.tiles:
        line_display = [cli[tile] for tile in line]
        print(line_display)


alphabet = string.ascii_uppercase


def redraw_board(window, board):
    size = board.size
    for i in range(size):
        for j in range(size):
            color = "#0C702C"
            piece_image = images[board.tiles[i][j]]
            elem = window.FindElement(key=(i, j))
            elem.Update(button_color=('white', color),
                        image_filename=piece_image, )
    window.Refresh()


def create_window(game_name, size, board):
    layout = [[sg.T('{}'.format(a), pad=((24, 23), 0), font='Any 13') for a in alphabet[:size]]]
    for i in range(size):
        row = []
        for j in range(size):
            color = "#0C702C"
            row.append(sg.RButton(' ', size=(8, 4), key=(i, j), pad=(0, 0), border_width=5, button_color=('white', color)))
        row.append(sg.T(str(size - i) + '   ', pad=((23, 0), 0), font='Any 13'))
        layout.append(row)

    window = sg.Window("{}".format(game_name), layout, auto_size_buttons=False, finalize=True)
    redraw_board(window, board)
    return window


def get_event(window):
    event, _ = window.read()
    if event in (None, 'Exit'):
        window.close()
        exit()
    return event


if __name__ == "__main__":
    import game

    size = 8
    game_board = game.init_board(size)
    window = create_window("Reversi", size, game_board)
    while True:
        event, _ = window.read()
        print(event)
        if event in (None, 'Exit'):
            break