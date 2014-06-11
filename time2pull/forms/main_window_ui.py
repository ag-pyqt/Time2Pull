# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Jun 11 18:40:11 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(539, 307)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/time2pull/icons/git-light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelRefresh = QtWidgets.QLabel(self.centralwidget)
        self.labelRefresh.setText("")
        self.labelRefresh.setObjectName("labelRefresh")
        self.horizontalLayout.addWidget(self.labelRefresh)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonAdd = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("add")
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("remove")
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout.addWidget(self.pushButtonRemove)
        self.pushButtonRefresh = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.pushButtonRefresh.setIcon(icon)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.horizontalLayout.addWidget(self.pushButtonRefresh)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.listWidgetRepos = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetRepos.setObjectName("listWidgetRepos")
        self.gridLayout.addWidget(self.listWidgetRepos, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("exit")
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("info")
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Time2Pull"))
        self.pushButtonAdd.setText(_translate("MainWindow", "Add "))
        self.pushButtonRemove.setText(_translate("MainWindow", "Remove"))
        self.pushButtonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setToolTip(_translate("MainWindow", "About Time2Pull"))

from . import resources_rc
