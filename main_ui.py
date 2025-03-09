# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStackedWidget, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(800, 600)
        self.actionLogin = QAction(mainWindow)
        self.actionLogin.setObjectName(u"actionLogin")
        self.actionExit = QAction(mainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAdd_modify_book = QAction(mainWindow)
        self.actionAdd_modify_book.setObjectName(u"actionAdd_modify_book")
        self.actionDashboard = QAction(mainWindow)
        self.actionDashboard.setObjectName(u"actionDashboard")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 801, 551))
        self.welcomePage = QWidget()
        self.welcomePage.setObjectName(u"welcomePage")
        self.backgroundLabel = QLabel(self.welcomePage)
        self.backgroundLabel.setObjectName(u"backgroundLabel")
        self.backgroundLabel.setGeometry(QRect(0, 0, 800, 600))
        self.backgroundLabel.setPixmap(QPixmap(u"assets/library_small.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel = QLabel(self.welcomePage)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(290, 200, 291, 21))
        font = QFont()
        font.setPointSize(20)
        self.timeLabel.setFont(font)
        self.titleLabel = QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setGeometry(QRect(310, 10, 221, 61))
        font1 = QFont()
        font1.setFamilies([u"Imprint MT Shadow"])
        font1.setPointSize(32)
        font1.setItalic(False)
        self.titleLabel.setFont(font1)
        self.titleLabel.setAutoFillBackground(False)
        self.stackedWidget.addWidget(self.welcomePage)
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.tableWidget = QTableWidget(self.mainPage)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, 90, 801, 471))
        self.pushButton = QPushButton(self.mainPage)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(710, 20, 75, 23))
        self.stackedWidget.addWidget(self.mainPage)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFIle = QMenu(self.menubar)
        self.menuFIle.setObjectName(u"menuFIle")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFIle.menuAction())
        self.menuFIle.addAction(self.actionLogin)
        self.menuFIle.addAction(self.actionDashboard)
        self.menuFIle.addSeparator()
        self.menuFIle.addAction(self.actionExit)

        self.retranslateUi(mainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Library app", None))
        self.actionLogin.setText(QCoreApplication.translate("mainWindow", u"Login", None))
        self.actionExit.setText(QCoreApplication.translate("mainWindow", u"Exit", None))
        self.actionAdd_modify_book.setText(QCoreApplication.translate("mainWindow", u"Add/modify book", None))
        self.actionDashboard.setText(QCoreApplication.translate("mainWindow", u"Dashboard", None))
        self.backgroundLabel.setText("")
        self.timeLabel.setText(QCoreApplication.translate("mainWindow", u"2025.03.08. 20:01:25", None))
        self.titleLabel.setText(QCoreApplication.translate("mainWindow", u"Library app", None))
        self.pushButton.setText(QCoreApplication.translate("mainWindow", u"PushButton", None))
        self.menuFIle.setTitle(QCoreApplication.translate("mainWindow", u"File", None))
    # retranslateUi

