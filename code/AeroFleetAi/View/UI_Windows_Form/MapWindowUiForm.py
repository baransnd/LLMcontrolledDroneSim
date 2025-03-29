# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MapWindowUiForm.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MapWindow(object):
    def setupUi(self, MapWindow):
        if not MapWindow.objectName():
            MapWindow.setObjectName(u"MapWindow")
        MapWindow.resize(1024, 768)
        self.centralwidget = QWidget(MapWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.verticalLayout.addWidget(self.label)

        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.webEngineView)

        self.labelCoordinates = QLabel(self.centralwidget)
        self.labelCoordinates.setObjectName(u"labelCoordinates")

        self.verticalLayout.addWidget(self.labelCoordinates)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonCancel = QPushButton(self.centralwidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonNext = QPushButton(self.centralwidget)
        self.pushButtonNext.setObjectName(u"pushButtonNext")

        self.horizontalLayout.addWidget(self.pushButtonNext)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MapWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MapWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 33))
        MapWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MapWindow)
        self.statusbar.setObjectName(u"statusbar")
        MapWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MapWindow)

        QMetaObject.connectSlotsByName(MapWindow)
    # setupUi

    def retranslateUi(self, MapWindow):
        MapWindow.setWindowTitle(QCoreApplication.translate("MapWindow", u"Map Window", None))
        self.label.setText(QCoreApplication.translate("MapWindow", u"Select a coordinate to configure the middle point of the search area and press the Next button to continue, the drones will be moved to this area", None))
        self.labelCoordinates.setText(QCoreApplication.translate("MapWindow", u"Latitude: , Longitude: ", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("MapWindow", u"Cancel", None))
        self.pushButtonNext.setText(QCoreApplication.translate("MapWindow", u"Next", None))
    # retranslateUi

