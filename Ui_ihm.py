# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Documents\Programmation\PublicProject\Basic UI for process on files and folders\ihm.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(642, 86)
        MainWindow.setMinimumSize(QtCore.QSize(642, 86))
        MainWindow.setMaximumSize(QtCore.QSize(642, 86))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_process = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_process.setGeometry(QtCore.QRect(240, 40, 75, 23))
        self.pushButton_process.setMaximumSize(QtCore.QSize(16777215, 16777211))
        self.pushButton_process.setObjectName("pushButton_process")
        self.pushButton_browse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browse.setGeometry(QtCore.QRect(560, 10, 75, 23))
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.label_done = QtWidgets.QLabel(self.centralwidget)
        self.label_done.setGeometry(QtCore.QRect(330, 40, 51, 20))
        self.label_done.setObjectName("label_done")
        self.label_process = QtWidgets.QLabel(self.centralwidget)
        self.label_process.setGeometry(QtCore.QRect(330, 40, 131, 21))
        self.label_process.setObjectName("label_process")
        self.fileEdit_path = FileEdit(self.centralwidget)
        self.fileEdit_path.setGeometry(QtCore.QRect(10, 10, 541, 20))
        self.fileEdit_path.setObjectName("fileEdit_path")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_browse, self.pushButton_process)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FileFolderProcess"))
        self.pushButton_process.setText(_translate("MainWindow", "process"))
        self.pushButton_browse.setText(_translate("MainWindow", "browse"))
        self.label_done.setText(_translate("MainWindow", "done !"))
        self.label_process.setText(_translate("MainWindow", "in process..."))
from main import FileEdit
