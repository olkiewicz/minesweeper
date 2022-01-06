import math
import random
from enum import Enum

import numpy as np


class Action(Enum):
    CHECK_AS_MINE = 1
    DISCOVER = 2


class Minesweeper:
    def __init__(self, size: int):
        self.game_over = False
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        #  0 - nothing, not discovered; -1 - mine;
        # -2 - checked as mine;         -3 nothing, discovered
        self.checked_as_mine = 0
        self.number_of_mines = 10

    def add_mines(self, x: int, y: int):
        _number_of_mines = 0

        while True:
            if _number_of_mines == self.number_of_mines:
                break

            mine_x = random.randint(0, self.size - 1)
            mine_y = random.randint(0, self.size - 1)

            if math.dist((x, y), (mine_x, mine_y)) <= 3.0:
                continue

            self.board[mine_x, mine_y] = -1
            _number_of_mines += 1

    def recalculate_board(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == -1:
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

                        if self.board[x_around, y_around] == -1:
                            mines_around += 1

                self.board[x, y] = mines_around + 10 if mines_around > 0 else mines_around

    def first_action(self, x: int, y: int):
        self.add_mines(x, y)
        self.recalculate_board()
        self.discover(x, y)

    def action(self, x: int, y: int, action: Action):
        value = self.board[x, y]
        if value == -3:
            return False

        if action == Action.DISCOVER:
            if value == -1:
                self.game_over = True
            elif value == -3:
                self.discover(x, y)

        elif action == Action.CHECK_AS_MINE:
            if self.board[x, y] == -2:
                self.board[x, y] = 0

            if self.checked_as_mine >= self.size:
                return

            self.board[x, y] = -2
            self.checked_as_mine += 1

            if self.checked_as_mine == self.number_of_mines and not np.any(self.board == 0):
                self.game_over = True

    def discover(self, x: int, y: int):
        value = self.board[x, y]
        if value == -1:
            self.game_over = True
            return False

        if value not in [0, -3]:
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
                    self.board[x_around, y_around] = -3
                    self.discover(x_around, y_around)
                elif around_value > 10:
                    self.board[x_around, y_around] -= 10

        self.board[x, y] = -3

    def __str__(self):
        return self.board.__str__().replace('0', '-').replace('-3', '  ').replace('-1', ' -')

    def __repr__(self):
        return self.board.__str__()
