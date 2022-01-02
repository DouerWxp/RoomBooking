# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.6


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(398, 296)
        self.login_button = QtWidgets.QDialogButtonBox(Login)
        self.login_button.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.login_button.setOrientation(QtCore.Qt.Horizontal)
        self.login_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.login_button.setObjectName("login_button")
        self.login_username = QtWidgets.QLineEdit(Login)
        self.login_username.setGeometry(QtCore.QRect(150, 90, 141, 21))
        self.login_username.setObjectName("login_username")
        self.login_password = QtWidgets.QLineEdit(Login)
        self.login_password.setGeometry(QtCore.QRect(150, 130, 141, 21))
        self.login_password.setObjectName("login_password")
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(40, 90, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.login_remember = QtWidgets.QCheckBox(Login)
        self.login_remember.setGeometry(QtCore.QRect(130, 180, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_remember.setFont(font)
        self.login_remember.setObjectName("login_remember")

        self.retranslateUi(Login)
        self.login_button.accepted.connect(Login.accept) # type: ignore
        self.login_button.rejected.connect(Login.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Dialog"))
        self.label.setText(_translate("Login", "username:"))
        self.label_2.setText(_translate("Login", "password: "))
        self.login_remember.setText(_translate("Login", "remember me"))
