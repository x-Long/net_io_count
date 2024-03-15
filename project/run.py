import os
import sys

import psutil
from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction, QDesktopWidget

from project.net_io_count_ui import Ui_Dialog
from project.path_manager import PathManager
from project.util.utils import NetCountThread, GlobalVariables


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.ui.show()
        self.createMenu()

    def createMenu(self):
        self.menu = QtWidgets.QMenu()
        self.showAction = QtWidgets.QAction("显示", self, triggered=self.show_window)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onIconClicked)

    def show_window(self):
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()

    def onIconClicked(self, reason):
        """
        :param reason: 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        """
        if reason == 2 or reason == 3:
            if self.ui.isMinimized() or not self.ui.isVisible():
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.show()


class MainWindow(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.net_count_thread = NetCountThread()
        self.net_count_thread.net_count_signal.connect(self.changge_net_io_value)
        self.net_count_thread.start()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.m_flag = False

    def showContextMenu(self, pos):
        menu = QMenu()

        for card_name in psutil.net_io_counters(pernic=True):
            if card_name == GlobalVariables.card_name:
                menu.addAction(QAction(QIcon(os.path.join(PathManager.icon_dir, "网卡.png")), card_name, self))
            else:
                menu.addAction(QAction(card_name, self))

        menu.addSeparator()
        menu.addAction(QAction(QIcon(os.path.join(PathManager.icon_dir, "退出.png")), "退出", self))

        action = menu.exec_(self.mapToGlobal(pos))

        if not action:
            return

        GlobalVariables.card_name = action.text()

        if action.text() == '退出':
            sys.exit()

    def changge_net_io_value(self, up, down):
        self.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnTopHint | Qt.Qt.Tool)
        self.label.setText(up)
        self.label_down.setText(down)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(Qt.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(Qt.Qt.ArrowCursor))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnTopHint | Qt.Qt.Tool)

    screen_geometry = QDesktopWidget().screenGeometry(0)
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    main_window.move(screen_width * 0.85, screen_height * 0.85)
    main_window.show()

    ti = TrayIcon(main_window)
    icon = QtGui.QIcon(os.path.join(PathManager.icon_dir, "logo.png"))
    ti.setIcon(icon)
    ti.setToolTip("流量监测工具")
    ti.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
