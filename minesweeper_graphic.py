import math
import random
from enum import Enum

import numpy as np


class ActionGraphic(Enum):
    CHECK_AS_MINE = 1
    DISCOVER = 2


class MinesweeperGraphic:
    def __init__(self, size: int):
        self.game_over = False
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        #  0 - nothing, not discovered; -91 - mine;
        # -92 - checked as mine;        -93 nothing, discovered
        self.checked_as_mine = 0
        self.number_of_mines = 10
        self.list_of_mines = []

    def add_mines(self, x: int, y: int):
        _number_of_mines = 0

        while True:
            if _number_of_mines == self.number_of_mines:
                break

            mine_x = random.randint(0, self.size - 1)
            mine_y = random.randint(0, self.size - 1)

            if math.dist((x, y), (mine_x, mine_y)) <= 3.0 or (mine_x, mine_y) in self.list_of_mines:
                continue

            self.board[mine_x, mine_y] = -91
            self.list_of_mines.append((mine_x, mine_y))
            _number_of_mines += 1

    def recalculate_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == -91:
                    continue

                mines_around = 0
                x_min = x - 1 if x > 0 else x
                x_max = x + 1 if x + 1 < self.size else x
                y_min = y - 1 if y > 0 else y
                y_max = y + 1 if y + 1 < self.size else y

                for x_around in range(x_min, x_max + 1):
                    for y_around in range(y_min, y_max + 1):
                        if x_around == x and y_around == y:
                            continue

                        if self.board[x_around, y_around] == -91:
                            mines_around += 1

                self.board[x, y] = mines_around + 10 if mines_around > 0 else mines_around

    def first_action(self, x: int, y: int):
        self.add_mines(x, y)
        self.recalculate_board()
        self.discover(x, y)

    def action(self, x: int, y: int, action: ActionGraphic):
        value = self.board[x, y]
        if value == -93:
            return False

        if action == ActionGraphic.DISCOVER:
            if value == -91:
                self.game_over = True
            # elif value == -93:
            else:
                self.discover(x, y)

        elif action == ActionGraphic.CHECK_AS_MINE:
            if 1 <= value <= 9:
                return

            if value == -92:
                if (x, y) in self.list_of_mines:
                    self.board[x, y] = -91
                else:
                    self.board[x, y] = 0
                return

            if self.checked_as_mine >= self.number_of_mines:
                return False

            self.board[x, y] = -92
            self.checked_as_mine += 1

            if self.checked_as_mine == self.number_of_mines and not np.any(self.board == 0) and not np.any(self.board == -91):
                # TODO: maybe we should check if all fields checked as mines are in list self.list_of_mines
                self.game_over = True

    def discover(self, x: int, y: int):
        # FIXME: algorithm has some bugs, but it works
        value = self.board[x, y]

        if value == -91:
            self.game_over = True
            return False

        if value not in [0, -93, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
            return

        if 10 < value <= 19:
            self.board[x, y] -= 10
            return

        x_min = x - 1 if x > 0 else x
        x_max = x + 1 if x + 1 < self.size else x
        y_min = y - 1 if y > 0 else y
        y_max = y + 1 if y + 1 < self.size else y

        for x_around in range(x_min, x_max + 1):
            for y_around in range(y_min, y_max + 1):
                if x_around == x and y_around == y:
                    continue

                around_value = self.board[x_around, y_around]

                if around_value == 0:
                    self.board[x_around, y_around] = -93
                    self.discover(x_around, y_around)

                elif around_value > 10:
                    self.board[x_around, y_around] -= 10
                    break

        self.board[x, y] = -93

    def are_all_mines_checked(self):
        if self.number_of_mines == self.checked_as_mine:
            list_of_checked_fields = []

            for x in range(self.size):
                for y in range(self.size):
                    value = self.board[x, y]

                    if value == -92:
                        if (x, y) not in self.list_of_mines:
                            return False

                        else:
                            list_of_checked_fields.append((x, y))

            if len(list_of_checked_fields) == self.number_of_mines:
                return True

        return False

    def __str__(self):
        return self.board.__str__() + '\n\n'  + self.board.__str__().replace('0', '-').replace('-93', '   ').replace('-91', '  -').replace('11', ' -').replace('12', ' -').replace('13', ' -').replace('14', ' -').replace('15', ' -').replace('-92', '  T')\
               + f'\n{self.game_over}, num_of_mines={self.checked_as_mine}' + ''.join([f'{mine}' for mine in self.list_of_mines])
        # return self.board.__str__().replace('0', '-').replace('-93', '   ').replace('-91', '   ').replace('11', '  ').replace('12', '  ').replace('13', '  ').replace('14', '  ')

    def __repr__(self):
        return self.board.__str__()
