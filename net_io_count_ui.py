

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(130, 50)
        Dialog.setStyleSheet("background:#0c0c0c")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 7, 0, 7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
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
        self.label_down = QtWidgets.QLabel(Dialog)
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

