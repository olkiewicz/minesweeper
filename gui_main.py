import sys
import threading

import PyQt5
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QPoint, QEvent, QRect, QMetaObject, QCoreApplication, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QStatusBar, QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLCDNumber, \
    QPushButton, QMenuBar

import time


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


class UiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"MainWindow")

        self.resize(800, 800)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.central_widget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(100, 100, 600, 600))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setGeometry(QRect(0, 0, 600, 600))
        self.frame = QFrame(self.gridLayoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.availableMines = QLCDNumber(self.central_widget)
        self.availableMines.setObjectName(u"availableMines")
        self.availableMines.setGeometry(QRect(120, 50, 161, 41))
        self.time = QLCDNumber(self.central_widget)
        self.time.setObjectName(u"time")
        self.time.setGeometry(QRect(530, 50, 161, 41))
        self.pushButton = QPushButton(self.central_widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(350, 50, 111, 41))
        self.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 843, 21))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.mine_icon = QIcon()
        self.mine_icon.addPixmap(QPixmap('mine_icon.png'))

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

        self.mines = []
        i = 0
        for x in range(6):
            row = []
            for y in range(6):
                push_button = QPushButton()
                push_button.setObjectName(f'[{x}][{y}]')
                push_button.setFixedSize(100, 100)
                push_button.clicked.connect(lambda state, z=x, t=y: self.on_click(z, t))
                self.gridLayout.addWidget(push_button, x, y)
                row.append(push_button)
                i += 1
            self.mines.append(row)

        self.time_start = -1
        self.timer_stop = False
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start / Reset", None))
    # retranslateUi

    def in_thread(self):
        while not self.timer_stop and self.time_start < 1000:
            time.sleep(1)
            self.time_start += 1
            self.time.display(self.time_start)

    def on_click(self, a, b):
        self.mines[a][b].setStyleSheet("background-color : #bfbfbf")
        self.mines[a][b].setText('')
        self.mines[a][b].setIcon(self.mine_icon)
        self.mines[a][b].setIconSize(QSize(30, 30))
        print(a, b)

        if self.time_start == -1:
            self.time_start = 0
            self.thread = threading.Thread(target=self.in_thread)
            self.thread.start()

    def handle_window_released(self, window_pos: QPoint, global_pos: QPoint):
        x = (window_pos.x() - 100) // 100
        y = (window_pos.y() - 100) // 100
        print(f'handle_window_released: {x}, {y}')

        if self.time_start == -1:
            self.time_start = 0
            self.thread = threading.Thread(target=self.in_thread)
            self.thread.start()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.timer_stop = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = UiMainWindow()
    my_win.show()

    mouse_observer = MouseObserver(my_win)
    mouse_observer.released.connect(my_win.handle_window_released)

    sys.exit(app.exec_())
