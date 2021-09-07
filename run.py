import psutil
from PyQt5 import QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCursor
from net_io_count_ui import Ui_Dialog
import sys
import time


class NetCountThread(QtCore.QThread):
    _signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(NetCountThread, self).__init__(parent)

    def speed_test(self):
        s1 = psutil.net_io_counters(pernic=True)['WLAN']
        time.sleep(1)
        s2 = psutil.net_io_counters(pernic=True)['WLAN']
        upload = s2.bytes_sent - s1.bytes_sent
        download = s2.bytes_recv - s1.bytes_recv
        return str('↑%.2f' % (upload / 1024)) + 'KB/s', str('↓%.2f' % (download / 1024)) + 'KB/s'

    def run(self):
        while True:
            up, down = self.speed_test()
            self._signal.emit(up, down)


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
        # 设置图标
        # self.setIcon(QtGui.QIcon("/path/icon"))
        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.show()


class Main_window(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.thread = NetCountThread()
        self.thread._signal.connect(self.changge_net_io_value)
        self.thread.start()
        self.setWindowFlags(QtCore.Qt.Tool)

    def changge_net_io_value(self, up, down):
        self.label.setText(up)
        self.label_down.setText(down)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  
            event.accept()
            self.setCursor(QCursor(Qt.Qt.OpenHandCursor)) 

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position) 
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.Qt.ArrowCursor))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnTopHint | Qt.Qt.Tool)
    main_window.show()
    ti = TrayIcon(main_window)
    ti.show()
    sys.exit(app.exec_())
