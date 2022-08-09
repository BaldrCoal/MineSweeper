import main
import random


def test_open():
    h, w = random.randint(2, 10), random.randint(2, 10)
    c = random.randint(0, h * w)
    game = main.Field(h, w, c)
    assert sum(sum(cell.is_open for cell in row) for row in game.field) == 0, \
        "After starting game all tiles must be closed"
    game.field[0][0].open()
    assert sum(sum(cell.is_open for cell in row) for row in game.field) == 1, \
        "Wrong number of opened tiles (must be 1)"
    game.field[0][1].open()
    assert sum(sum(cell.is_open for cell in row) for row in game.field) == 2, \
        "Wrong number of opened tiles (must be 2)"
    game.field[1][0].open()
    assert sum(sum(cell.is_open for cell in row) for row in game.field) == 3, \
        "Wrong number of opened tiles (must be 2)"
    game.field[1][1].open()
    assert sum(sum(cell.is_open for cell in row) for row in game.field) == 4, \
        "Wrong number of opened tiles (must be 2)"


def test_mines_count():
    for _ in range(100):
        h, w = random.randint(1, 10), random.randint(1, 10)
        c = random.randint(0, h * w)
        game = main.Field(h, w, c)

        game.start_game()
        assert c == sum([sum([cell.mine for cell in row]) for row in game.field]), "Mine count doesnt match"


def test_get_neighbours():
    h, w = 5, 3
    c = 5
    game = main.Field(h, w, c)
    game.start_game()
    for row in game.field:
        for cell in row:
            cell.mine = False

    assert game._mines_around(0, 1) == 0 and \
           game._mines_around(1, 0) == 0 and \
           game._mines_around(1, 1) == 0, "Wrong number of neigh mines"

    game.field[0][0].mine = True
    assert game._mines_around(0, 1) == 1 and \
           game._mines_around(1, 0) == 1 and \
           game._mines_around(1, 1) == 1, "Wrong number of neigh mines"

    game.field[2][2].mine = True
    assert game._mines_around(0, 1) == 1 and \
           game._mines_around(1, 0) == 1 and \
           game._mines_around(1, 1) == 2, "Wrong number of neigh mines"


def test_lose():
    random.seed(1)
    h, w = 5, 5
    m = 5
    game = main.Field(h, w, m)
    game.start_game()
    assert game.click_on_field(0, 2, left_mouse=True) == 0, "Failed lose case"
