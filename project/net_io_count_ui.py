import os.path

from PyQt5 import QtCore, QtGui, QtWidgets

from project.path_manager import PathManager

background = os.path.join(PathManager.icon_dir, "bg.jpg")


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(130, 50)

        layout = QtWidgets.QVBoxLayout(Dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QtWidgets.QFrame()
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("QFrame#frame{border-image: url('" + background.replace("\\", "/") + "');}")

        layout.addWidget(self.frame)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 7, 0, 7)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#faab23")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_down = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.label_down.setFont(font)
        self.label_down.setStyleSheet("color:#72b42c")
        self.label_down.setAlignment(QtCore.Qt.AlignCenter)
        self.label_down.setObjectName("label_down")
        self.verticalLayout.addWidget(self.label_down)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "xlong 流量统计"))
        self.label.setText(_translate("Dialog", "↑0.00KB/s"))
        self.label_down.setText(_translate("Dialog", "↓0.00KB/s"))
