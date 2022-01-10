import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QStatusBar, QApplication, QMainWindow


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class UiMainWindow(object):

    def __init__(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")

        main_window.resize(800, 800)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.central_widget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(100, 120, 605, 605))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setGeometry(QRect(0, 0, 605, 605))
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
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 843, 21))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.mines = []
        i = 0
        for x in range(6):
            row = []
            for y in range(6):
                push_button = QPushButton(f'[{x}][{y}]')
                push_button.setFixedSize(100, 100)
                push_button.clicked.connect(lambda z=x, t=y: self.on_click(z, t))
                # QObject.connect(push_button, self.on_click)
                self.gridLayout.addWidget(push_button, x, y)
                row.append(push_button)
                i += 1
            self.mines.append(row)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start / Reset", None))
    # retranslateUi

    @pyqtSlot()
    def on_click(self, a, b):
        print(a, b)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    my_win = UiMainWindow(win)
    win.show()
    sys.exit(app.exec_())
