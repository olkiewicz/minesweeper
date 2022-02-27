import math
import random
from enum import Enum

import numpy as np


class Field(Enum):
    NOT_DISCOVERED = 0
    MINE = -91
    CHECKED_AS_MINE = -92
    DISCOVERED = -93
    ONE_MINE_AROUND = 11
    TWO_MINES_AROUND = 12
    THREE_MINES_AROUND = 13
    FOUR_MINES_AROUND = 14
    FIVE_MINES_AROUND = 15
    SIX_MINES_AROUND = 16
    ONE_MINE_AROUND_DISCOVERED = 1
    TWO_MINES_AROUND_DISCOVERED = 2
    THREE_MINES_AROUND_DISCOVERED = 3
    FOUR_MINES_AROUND_DISCOVERED = 4
    FIVE_MINES_AROUND_DISCOVERED = 5
    SIX_MINES_AROUND_DISCOVERED = 6

    @staticmethod
    def discover(field):
        return Field(field.value - 10)


class ActionGraphic(Enum):
    CHECK_AS_MINE = 1
    DISCOVER = 2


class MinesweeperGraphic:
    def __init__(self, size: int):
        self.game_over = False
        self.size = size
        self.board = np.zeros((size, size), dtype=Field)
        for x in range(9):
            for y in range(9):
                self.board[x, y] = Field.NOT_DISCOVERED

        self.checked_as_mine = 0
        self.number_of_mines = 10
        self.list_of_mines = []
        self.checked_fields = {}

    def add_mines(self, x: int, y: int):
        _number_of_mines = 0

        while True:
            if _number_of_mines == self.number_of_mines:
                break

            mine_x = random.randint(0, self.size - 1)
            mine_y = random.randint(0, self.size - 1)

            if math.dist((x, y), (mine_x, mine_y)) <= 3.0 or (mine_x, mine_y) in self.list_of_mines:
                continue

            self.board[mine_x, mine_y] = Field.MINE
            self.list_of_mines.append((mine_x, mine_y))
            _number_of_mines += 1

    def recalculate_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == Field.MINE:
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

                        if self.board[x_around, y_around] == Field.MINE:
                            mines_around += 1

                self.board[x, y] = Field(mines_around + 10) if mines_around > 0 else Field.NOT_DISCOVERED

    def first_action(self, x: int, y: int):
        self.add_mines(x, y)
        self.recalculate_board()
        self.discover(x, y)

    def action(self, x: int, y: int, action: ActionGraphic):
        value = self.board[x, y]
        if value == Field.DISCOVERED:
            return False

        if action == ActionGraphic.DISCOVER:
            if value == Field.MINE:
                self.game_over = True

            else:
                self.discover(x, y)

        elif action == ActionGraphic.CHECK_AS_MINE:
            if Field.ONE_MINE_AROUND_DISCOVERED.value <= value.value <= Field.SIX_MINES_AROUND_DISCOVERED.value:
                return

            if value == Field.CHECKED_AS_MINE:
                self.checked_as_mine -= 1

                if (x, y) in self.list_of_mines:
                    self.board[x, y] = Field.MINE

                else:
                    if (x, y) in self.checked_fields.keys():
                        self.board[x, y] = self.checked_fields[(x, y)]
                        self.checked_fields.pop((x, y))
                return

            self.checked_fields[(x, y)] = value
            if self.checked_as_mine >= self.number_of_mines:
                return False

            self.board[x, y] = Field.CHECKED_AS_MINE
            self.checked_as_mine += 1

            if self.checked_as_mine == self.number_of_mines and not np.any(self.board == Field.NOT_DISCOVERED) and not np.any(self.board == Field.MINE):
                self.game_over = True

    def discover(self, x: int, y: int):
        value: Field = self.board[x, y]

        if value == Field.MINE:
            self.game_over = True
            return False

        if value not in [Field.NOT_DISCOVERED, Field.DISCOVERED, Field.ONE_MINE_AROUND, Field.TWO_MINES_AROUND, Field.THREE_MINES_AROUND, Field.FOUR_MINES_AROUND, Field.FIVE_MINES_AROUND, Field.SIX_MINES_AROUND]:
            return

        if Field.ONE_MINE_AROUND.value <= value.value <= Field.SIX_MINES_AROUND.value:
            self.board[x, y] = Field.discover(value)
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

                if around_value == Field.NOT_DISCOVERED:
                    self.board[x_around, y_around] = Field.DISCOVERED
                    self.discover(x_around, y_around)

                elif around_value.value >= Field.ONE_MINE_AROUND.value:
                    self.board[x_around, y_around] = Field.discover(around_value)

        self.board[x, y] = Field.DISCOVERED

    def are_all_mines_checked(self):
        if self.number_of_mines == self.checked_as_mine:
            list_of_checked_fields = []

            for x in range(self.size):
                for y in range(self.size):
                    value = self.board[x, y]

                    if value == Field.CHECKED_AS_MINE:
                        if (x, y) not in self.list_of_mines:
                            return False

                        else:
                            list_of_checked_fields.append((x, y))

            if len(list_of_checked_fields) == self.number_of_mines:
                return True

        return False

    def __str__(self):
        return self.board.__str__()

    def __repr__(self):
        return self.board.__str__()
