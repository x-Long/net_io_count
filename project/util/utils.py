import socket
import threading
import time

import psutil
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


def get_net_card() -> dict:
    name = ip = ''
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in range(0, len(v)):
            if v[item][0] == 2 and get_ip() in v[item][1]:
                name = k
                ip = v[item][1]
                break
    info = {'net_card_name': name, 'ip': ip}
    return info


class GlobalVariables:
    card_name = get_net_card()["net_card_name"]


class NetCardThread(threading.Thread):

    def __init__(self):
        super(NetCardThread, self).__init__()
        self.daemon = True
        self.net_card_name = ""

    def run(self):
        while True:
            self.net_card_name = get_net_card()["net_card_name"]
            time.sleep(1)


class NetCountThread(QtCore.QThread):
    net_count_signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(NetCountThread, self).__init__(parent)
        self.net_card_thread = NetCardThread()
        self.net_card_thread.start()

    def net_io_count(self):
        net_card_name = GlobalVariables.card_name
        if not net_card_name:
            return '↑0.00KB/s', '↓0.00KB/s',
        s1 = psutil.net_io_counters(pernic=True)[net_card_name]
        time.sleep(1)
        s2 = psutil.net_io_counters(pernic=True)[net_card_name]
        upload = s2.bytes_sent - s1.bytes_sent
        download = s2.bytes_recv - s1.bytes_recv
        return str('↑%.2f' % (upload / 1024)) + 'KB/s', str('↓%.2f' % (download / 1024)) + 'KB/s'

    def run(self):
        while True:
            up, down = self.net_io_count()
            self.net_count_signal.emit(up, down)
