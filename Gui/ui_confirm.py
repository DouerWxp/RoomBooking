# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm.ui'
#
# Created by: PyQt5 UI code generator 5.15.6


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Confirm(object):
    def setupUi(self, Confirm):
        Confirm.setObjectName("Confirm")
        Confirm.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Confirm)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Confirm)
        self.label.setGeometry(QtCore.QRect(60, 50, 271, 71))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Confirm)
        self.textBrowser.setGeometry(QtCore.QRect(20, 130, 351, 91))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Confirm)
        self.buttonBox.accepted.connect(Confirm.accept) # type: ignore
        self.buttonBox.rejected.connect(Confirm.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Confirm)

    def retranslateUi(self, Confirm):
        _translate = QtCore.QCoreApplication.translate
        Confirm.setWindowTitle(_translate("Confirm", "Dialog"))
        self.label.setText(_translate("Confirm", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Are You Confirm </span></p><p align=\"center\"><span style=\" font-size:12pt;\">The Delete Operation?</span></p></body></html>"))
