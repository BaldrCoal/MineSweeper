import random
import time

random.seed(1)


class Cell:
    def __init__(self):
        self.mine = False
        self.around_mines = 0
        self.is_open = False
        self.is_flag = False

    def open(self):
        self.is_open = True

    def flag(self):
        self.is_flag = not self.is_flag

    def __str__(self):
        if self.is_flag:
            return 'F'
        if not self.is_open:
            return '#'
        if self.mine:
            return '*'
        if self.around_mines == 0:
            return '-'
        return f'{self.around_mines}'


class Field:
    def __init__(self, height: int, width: int, mine_count: int):
        self.height: int = height
        self.width: int = width
        self.mine_count: int = mine_count
        self.field: list[list[Cell]] = [[Cell() for _ in range(width)] for _ in range(height)]
        self.lose = False
        self.win = False
        self.game_is_continues = False

    def start_game(self) -> None:
        self._set_mines()
        self.game_is_continues = True

    def click_on_field(self, x: int, y: int, left_mouse=True):
        print(f"{self.game_is_continues=}, {self.is_win()=}, {self.lose=}")
        if not self.game_is_continues:
            return

        if left_mouse:
            if not self.field[x][y].is_flag:
                self.open_cell(x, y)
                print('открыли клетку')
                if self.is_lose(x, y):
                    self.show_field()
                    self.game_is_continues = False
                    print('Вы Проиграли')
                    return 0

        else:
            self.flag_cell(x, y)

        self.show_field()

        if self.is_win():
            self.game_is_continues = False
            print('Поздравляю, вы выиграли')
            return 1

    def open_cell(self, x: int, y: int) -> None:
        self.field[x][y].open()

        # Алгоритм открывания соседних клеток с 0 мин по соседству и их соседей (страшный)
        if self.field[x][y].around_mines == 0 and self.field[x][y].mine is False:
            for i in range(max(0, x - 1), min(self.height, x + 2)):
                for j in range(max(0, y - 1), min(self.width, y + 2)):
                    if i == x and j == y:
                        continue
                    if self.field[i][j].mine is False and self.field[i][j].around_mines == 0 \
                            and self.field[i][j].is_open is False:
                        self.open_cell(i, j)
                    for k in range(max(0, i - 1), min(self.height, i + 2)):
                        for l in range(max(0, j - 1), min(self.width, j + 2)):
                            self.field[i][j].open()

    def flag_cell(self, x: int, y: int) -> None:
        self.field[x][y].flag()

    def show_field(self) -> None:
        for x in self.field:
            for y in x:
                print(y, end=' ')
            print()
        print()

    def is_lose(self, x: int, y: int) -> bool:
        if self.field[x][y].mine:
            self.lose = True
            return True
        return False

    def is_win(self) -> bool:
        count_flaged_mines = 0
        count_open_cells = 0
        for line in self.field:
            for cell in line:

                if cell.mine and cell.is_flag:
                    count_flaged_mines += 1

                elif not cell.mine and cell.is_open:
                    count_open_cells += 1

        if count_flaged_mines == self.mine_count and count_open_cells == (
                self.height * self.width - self.mine_count):
            self.win = True
            return True
        return False

    def _set_mines(self) -> None:
        # Создание списка с рандомными координатами
        empty_field = list()
        for x in range(self.height):
            for y in range(self.width):
                empty_field.append((x, y))
        rnd_coord = tuple(random.sample(empty_field, self.mine_count))
        for x, y in rnd_coord:
            self.field[x][y].mine = True

        # Подсчет количества мин по соседству в клетке
        for x in range(self.height):
            for y in range(self.width):
                if self.field[x][y].mine:
                    continue
                else:
                    self.field[x][y].around_mines = self._mines_around(x, y)

    def _mines_around(self, x: int, y: int) -> int:
        cnt = 0
        for x_i in range(max(0, x - 1), min(self.height, x + 2)):
            for y_i in range(max(0, y - 1), min(self.width, y + 2)):
                if x_i == x and y_i == y:
                    continue
                if self.field[x_i][y_i].mine:
                    cnt += 1
        return cnt


if __name__ == "__main__":
    start = time.time()
    MineSweeper = Field(5, 5, 5)
    MineSweeper.start_game()
    # MineSweeper.click_on_field(4, 0, left_mouse=True)
    # MineSweeper.click_on_field(0, 2, right_mouse=True)
    # MineSweeper.click_on_field(0, 3, left_mouse=True)
    # MineSweeper.click_on_field(0, 4, right_mouse=True)
    # MineSweeper.click_on_field(1, 3, right_mouse=True)
    # MineSweeper.click_on_field(1, 4, left_mouse=True)
    # MineSweeper.click_on_field(2, 3, left_mouse=True)
    # MineSweeper.click_on_field(2, 4, left_mouse=True)
    # MineSweeper.click_on_field(3, 3, right_mouse=True)
    # MineSweeper.click_on_field(3, 3, left_mouse=True)
    # MineSweeper.click_on_field(3, 4, left_mouse=True)
    # MineSweeper.click_on_field(4, 3, left_mouse=True)
    # MineSweeper.click_on_field(4, 4, right_mouse=True)
    end = time.time()
    print(f'{end-start}')