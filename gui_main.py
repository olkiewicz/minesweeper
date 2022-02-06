import sys
import threading

import PyQt5
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QPoint, QEvent, QRect, QCoreApplication, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QStatusBar, QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLCDNumber, \
    QPushButton, QMenuBar, QMessageBox

import time

from minesweeper_graphic import MinesweeperGraphic, ActionGraphic, Field


class MouseObserver(PyQt5.QtCore.QObject):
    pressed = pyqtSignal(QPoint, QPoint)
    released = pyqtSignal(QPoint, QPoint)
    moved = pyqtSignal(QPoint, QPoint)

    def __init__(self, window):
        super().__init__(window)
        self._window = window

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if self.window is obj:
            if event.type() == QEvent.MouseButtonPress:
                self.pressed.emit(event.pos(), event.globalPos())
            elif event.type() == QEvent.MouseMove:
                self.moved.emit(event.pos(), event.globalPos())
            elif event.type() == QEvent.MouseButtonRelease:
                self.released.emit(event.pos(), event.globalPos())
        return super().eventFilter(obj, event)


class ResultMessageBox(QMessageBox):
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(ResultMessageBox, self).resizeEvent(event)
        self.setFixedSize(150, 150)
        self.setWindowTitle(' ')


class UiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.tile_size = 50

        self.thread: threading.Thread = threading.Thread(target=self.timer)

        if not self.objectName():
            self.setObjectName(u"MainWindow")

        self.resize(650, 650)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.central_widget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(100, 100, 450, 450))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setGeometry(QRect(0, 0, 450, 450))
        self.frame = QFrame(self.gridLayoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.availableMines = QLCDNumber(self.central_widget)
        self.availableMines.setObjectName(u"availableMines")
        self.availableMines.setGeometry(QRect(100, 25, 100, 50))
        self.availableMines.display(10)
        self.time = QLCDNumber(self.central_widget)
        self.time.setObjectName(u"time")
        self.time.setGeometry(QRect(450, 25, 100, 50))
        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setGeometry(QRect(275, 25, 100, 50))
        self.reset_button.clicked.connect(self.reset)
        self.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 100, 10))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.checked_mine_icon = QIcon()
        self.checked_mine_icon.addPixmap(QPixmap('checked_mine_icon.png'))
        self.mine_icon = QIcon()
        self.mine_icon.addPixmap(QPixmap('mine_icon.png'))
        self.exploded_mine_icon = QIcon()
        self.exploded_mine_icon.addPixmap(QPixmap('exploded_mine_icon.png'))

        self.retranslate_ui(self)

        self.mines = []
        self.draw_field()

        self.time_start = -1
        self.timer_stop = False

        self.first_action = True
        self.game_engine = MinesweeperGraphic(9)

    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"Reset", None))

    def draw_field(self):
        for x in range(9):
            row = []
            for y in range(9):
                push_button = QPushButton()
                push_button.setObjectName(f'[{x}][{y}]')
                push_button.setStyleSheet("background-color : #e8e8e8")
                push_button.setFixedSize(self.tile_size, self.tile_size)
                push_button.clicked.connect(lambda state, z=x, t=y: self.on_left_click(z, t))
                self.gridLayout.addWidget(push_button, x, y)
                row.append(push_button)

            self.mines.append(row)

    def timer(self):
        while not self.timer_stop and self.time_start < 1000:
            if self.timer_stop:
                break

            time.sleep(1)
            self.time_start += 1
            self.time.display(self.time_start)

    def on_left_click(self, a, b):
        if self.first_action:
            self.first_action = False
            self.game_engine.first_action(a, b)

            if self.thread is None:
                self.thread = threading.Thread(target=self.timer)
                self.time_start = 0
                self.thread.start()

        elif self.game_engine.game_over:
            return

        else:
            self.game_engine.action(a, b, ActionGraphic.DISCOVER)

        self.handle_after_action(ActionGraphic.DISCOVER, a, b)

    def on_right_click(self, window_pos: QPoint):
        if self.first_action or self.game_engine.game_over:
            return

        y = (window_pos.x() - 100) // self.tile_size
        x = (window_pos.y() - 100) // self.tile_size

        if 0 <= x < 9 and 0 <= y < 9:
            if self.game_engine.board[x, y] == Field.CHECKED_AS_MINE:
                self.game_engine.checked_as_mine -= 1

                if (x, y) in self.game_engine.list_of_mines:
                    self.game_engine.board[x, y] = Field.MINE

                else:
                    self.game_engine.board[x, y] = Field.NOT_DISCOVERED

            else:
                self.game_engine.action(x, y, ActionGraphic.CHECK_AS_MINE)

        self.handle_after_action(ActionGraphic.CHECK_AS_MINE)

    def paint_tile_as_discovered(self, x, y):
        self.mines[x][y].setStyleSheet("background-color : #c8c8c8")

    def paint_tile_as_checked(self, x, y):
        self.mines[x][y].setText('')
        self.mines[x][y].setIcon(self.checked_mine_icon)
        self.mines[x][y].setIconSize(QSize(self.tile_size - 4, self.tile_size - 4))

    def paint_tile_as_number(self, x, y, number: int):
        self.mines[x][y].setStyleSheet("background-color : #c8c8c8")
        font: QFont = self.mines[x][y].font()
        font.setPointSize(24)
        self.mines[x][y].setFont(font)
        self.mines[x][y].setText(f'{number}')

    def paint_default_tile(self, x: int, y: int):
        self.mines[x][y].setStyleSheet("background-color : #e8e8e8")
        self.mines[x][y].setText('')
        self.mines[x][y].setIcon(QIcon())

    def paint_all_mines(self, x: int, y: int):
        self.mines[x][y].setIcon(self.exploded_mine_icon)
        self.mines[x][y].setIconSize(QSize(self.tile_size, self.tile_size))

        for mine_x, mine_y in self.game_engine.list_of_mines:
            if mine_x == x and mine_y == y:
                continue

            self.mines[mine_x][mine_y].setIcon(self.mine_icon)
            self.mines[mine_x][mine_y].setIconSize(QSize(self.tile_size - 4, self.tile_size - 4))

    def refresh_tiles(self):
        self.availableMines.display(self.game_engine.number_of_mines - self.game_engine.checked_as_mine)

        for x in range(9):
            for y in range(9):
                value = self.game_engine.board[x, y]

                if value == Field.DISCOVERED:
                    self.paint_tile_as_discovered(x, y)

                elif 1 <= value.value < 9:
                    self.paint_tile_as_number(x, y, value.value)

                elif value == Field.CHECKED_AS_MINE:
                    self.paint_tile_as_checked(x, y)

                elif value in [Field.NOT_DISCOVERED, Field.MINE]:
                    self.paint_default_tile(x, y)
        print(self.game_engine.__str__())

    def handle_after_action(self, action: ActionGraphic, x: int = -1, y: int = -1):
        try:
            self.refresh_tiles()

            if self.game_engine.game_over:
                self.timer_stop = True

                msg = ResultMessageBox()

                if action == ActionGraphic.DISCOVER:
                    self.paint_all_mines(x, y)
                    self.statusbar.showMessage('You lose')
                    msg.setText('You lose')
                    msg.setIcon(QMessageBox.Critical)

                elif self.game_engine.are_all_mines_checked():
                    self.statusbar.showMessage('You win!')
                    msg.setText('You win')
                    msg.setIcon(QMessageBox.Information)

                msg.exec_()
        except BaseException as error:
            print(error)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.timer_stop = True

    def reset(self):
        self.game_engine = MinesweeperGraphic(9)
        self.timer_stop = False
        self.thread = None
        self.time_start = -1
        self.first_action = True
        self.refresh_tiles()
        self.time.display(0)
        self.availableMines.display(self.game_engine.number_of_mines)
        self.statusbar.showMessage('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_window = UiMainWindow()
    my_window.show()

    mouse_observer = MouseObserver(my_window)
    mouse_observer.pressed.connect(my_window.on_right_click)

    sys.exit(app.exec_())
