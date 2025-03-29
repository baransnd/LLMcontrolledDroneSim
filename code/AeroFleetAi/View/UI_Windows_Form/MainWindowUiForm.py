# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowUiForm.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSplitter, QStatusBar, QTextBrowser,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1306, 776)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.actionPlace_new_Object = QAction(MainWindow)
        self.actionPlace_new_Object.setObjectName(u"actionPlace_new_Object")
        self.actionDelete_Object = QAction(MainWindow)
        self.actionDelete_Object.setObjectName(u"actionDelete_Object")
        self.actionAdd_one_Drone = QAction(MainWindow)
        self.actionAdd_one_Drone.setObjectName(u"actionAdd_one_Drone")
        self.actionAdd_two_Drone = QAction(MainWindow)
        self.actionAdd_two_Drone.setObjectName(u"actionAdd_two_Drone")
        self.actionAdd_three_Drone = QAction(MainWindow)
        self.actionAdd_three_Drone.setObjectName(u"actionAdd_three_Drone")
        self.actionAdd_four_Drone = QAction(MainWindow)
        self.actionAdd_four_Drone.setObjectName(u"actionAdd_four_Drone")
        self.actionAdd_five_Drone = QAction(MainWindow)
        self.actionAdd_five_Drone.setObjectName(u"actionAdd_five_Drone")
        self.actionList_Drones = QAction(MainWindow)
        self.actionList_Drones.setObjectName(u"actionList_Drones")
        self.actionFree_Camera = QAction(MainWindow)
        self.actionFree_Camera.setObjectName(u"actionFree_Camera")        
        self.actionChange_Map = QAction(MainWindow)
        self.actionChange_Map.setObjectName(u"actionChange_Map")
        self.actionTest_One = QAction(MainWindow)
        self.actionTest_One.setObjectName(u"actionTest_One")
        self.actionTest_Two = QAction(MainWindow)
        self.actionTest_Two.setObjectName(u"actionTest_Two")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.menuLayout = QHBoxLayout()
        self.menuLayout.setObjectName(u"menuLayout")
        self.menubar = QMenuBar(self.centralwidget)
        self.menubar.setObjectName(u"menubar")
        self.menuObjectOptions = QMenu(self.menubar)
        self.menuObjectOptions.setObjectName(u"menuObjectOptions")
        self.menuDroneOptions = QMenu(self.menubar)
        self.menuDroneOptions.setObjectName(u"menuDroneOptions")
        self.menuInstructions = QMenu(self.menubar)
        self.menuInstructions.setObjectName(u"menuInstructions")
        self.menuAdd_Drone = QMenu(self.menuDroneOptions)
        self.menuAdd_Drone.setObjectName(u"menuAdd_Drone")
        self.menuDelete_Drone = QMenu(self.menuDroneOptions)
        self.menuDelete_Drone.setObjectName(u"menuDelete_Drone")
        self.menuManual_Control = QMenu(self.menuInstructions)
        self.menuManual_Control.setObjectName(u"menuManual_Control")
        self.menuChangeView = QMenu(self.menubar)
        self.menuChangeView.setObjectName(u"menuChangeView")
        self.menuGet_Drone_Position = QMenu(self.menuInstructions)
        self.menuGet_Drone_Position.setObjectName(u"menuGet_Drone_Position")
        self.menuGet_Drone_GPS = QMenu(self.menuInstructions)
        self.menuGet_Drone_GPS.setObjectName(u"menuGet_Drone_GPS")
        
        
        

        self.menuLayout.addWidget(self.menubar)

        self.toolBar = QToolBar(self.centralwidget)
        self.toolBar.setObjectName(u"toolBar")
        self.menuTest = QMenu(self.toolBar)
        self.menuTest.setObjectName(u"menuTestTest")                  # Kolin: this is a Test bar for me to test codes.
        


        self.menuLayout.addWidget(self.toolBar)


        self.verticalLayout.addLayout(self.menuLayout)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setOpaqueResize(False)
        self.splitter.setChildrenCollapsible(False)
        self.widget_left = QWidget(self.splitter)
        self.widget_left.setObjectName(u"widget_left")
        self.verticalLayout_left = QVBoxLayout(self.widget_left)
        self.verticalLayout_left.setObjectName(u"verticalLayout_left")
        self.verticalLayout_left.setContentsMargins(0, 0, 0, 0)
        self.label_image = QLabel(self.widget_left)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy)
        self.label_image.setMinimumSize(QSize(1000, 600))

        self.verticalLayout_left.addWidget(self.label_image)

        self.splitter.addWidget(self.widget_left)
        self.widget_right = QWidget(self.splitter)
        self.widget_right.setObjectName(u"widget_right")
        self.verticalLayout_right = QVBoxLayout(self.widget_right)
        self.verticalLayout_right.setObjectName(u"verticalLayout_right")
        self.verticalLayout_right.setContentsMargins(0, 0, 0, 0)
        self.chatLabel = QLabel(self.widget_right)
        self.chatLabel.setObjectName(u"chatLabel")

        self.verticalLayout_right.addWidget(self.chatLabel)

        self.textBrowser = QTextBrowser(self.widget_right)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(250, 450))

        self.verticalLayout_right.addWidget(self.textBrowser)

        self.label_user = QLabel(self.widget_right)
        self.label_user.setObjectName(u"label_user")

        self.verticalLayout_right.addWidget(self.label_user)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_input = QLineEdit(self.widget_right)
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setMinimumSize(QSize(200, 40))

        self.horizontalLayout.addWidget(self.lineEdit_input)

        self.pushButton_2 = QPushButton(self.widget_right)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioInputMicrophone))
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(35, 35))

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_right.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.widget_right)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuObjectOptions.menuAction())
        self.menubar.addAction(self.menuDroneOptions.menuAction())
        self.menubar.addAction(self.menuChangeView.menuAction())
        self.menubar.addAction(self.menuInstructions.menuAction())
        
        self.menuObjectOptions.addAction(self.actionPlace_new_Object)
        self.menuObjectOptions.addAction(self.actionDelete_Object)
        self.menuDroneOptions.addAction(self.menuAdd_Drone.menuAction())
        self.menuDroneOptions.addAction(self.menuDelete_Drone.menuAction())
        self.menuInstructions.addAction(self.menuManual_Control.menuAction())
        self.menuInstructions.addAction(self.menuGet_Drone_Position.menuAction())
        self.menuInstructions.addAction(self.menuGet_Drone_GPS.menuAction())
        self.menuInstructions.addAction(self.actionList_Drones)
        
        
        self.menuAdd_Drone.addAction(self.actionAdd_one_Drone)
        self.menuAdd_Drone.addAction(self.actionAdd_two_Drone)
        self.menuAdd_Drone.addAction(self.actionAdd_three_Drone)
        self.menuAdd_Drone.addAction(self.actionAdd_four_Drone)
        self.menuAdd_Drone.addAction(self.actionAdd_five_Drone)
        self.menuChangeView.addAction(self.actionFree_Camera)
        

        self.toolBar.addAction(self.actionChange_Map)
        self.toolBar.addAction(self.menuTest.menuAction())
        self.menuTest.addAction(self.actionTest_One)
        self.menuTest.addAction(self.actionTest_Two)
        
        

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AeroFleetAI", None))
        self.actionPlace_new_Object.setText(QCoreApplication.translate("MainWindow", u"Place new Object", None))
        self.actionDelete_Object.setText(QCoreApplication.translate("MainWindow", u"Delete Object", None))
        self.actionAdd_one_Drone.setText(QCoreApplication.translate("MainWindow", u"Add 1 drone", None))
        self.actionAdd_two_Drone.setText(QCoreApplication.translate("MainWindow", u"Add 2 drones", None))
        self.actionAdd_three_Drone.setText(QCoreApplication.translate("MainWindow", u"Add 3 drones", None))
        self.actionAdd_four_Drone.setText(QCoreApplication.translate("MainWindow", u"Add 4 drones", None))
        self.actionAdd_five_Drone.setText(QCoreApplication.translate("MainWindow", u"Add 5 drones", None))
        self.actionList_Drones.setText(QCoreApplication.translate("MainWindow", u"List all the drones", None))
        self.actionFree_Camera.setText(QCoreApplication.translate("MainWindow", u"Free Camera", None))
        self.actionTest_One.setText(QCoreApplication.translate("MainWindow", u"Test 1", None))
        self.actionTest_Two.setText(QCoreApplication.translate("MainWindow", u"Test 2", None))
        self.actionChange_Map.setText(QCoreApplication.translate("MainWindow", u"Reset Search Area", None))

        self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))       
        self.menuObjectOptions.setTitle(QCoreApplication.translate("MainWindow", u"Object Options", None))
        self.menuDroneOptions.setTitle(QCoreApplication.translate("MainWindow", u"Drone Options", None))
        self.menuInstructions.setTitle(QCoreApplication.translate("MainWindow", u"Instructions", None))
        self.menuAdd_Drone.setTitle(QCoreApplication.translate("MainWindow", u"Add Drone", None))
        self.menuDelete_Drone.setTitle(QCoreApplication.translate("MainWindow", u"Delete Drone", None))
        self.menuManual_Control.setTitle(QCoreApplication.translate("MainWindow", u"Manual Control", None))
        self.menuGet_Drone_Position.setTitle(QCoreApplication.translate("MainWindow", u"Get position(Vector 3D) of drone", None))
        self.menuGet_Drone_GPS.setTitle(QCoreApplication.translate("MainWindow", u"Get GPS of drone", None))
        
        self.menuChangeView.setTitle(QCoreApplication.translate("MainWindow", u"Change View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.label_image.setStyleSheet(QCoreApplication.translate("MainWindow", u"background-color: #d3d3d3;", None))
        self.label_image.setText("")
        self.chatLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"color: yellow; font-weight: bold;", None))
        self.chatLabel.setText(QCoreApplication.translate("MainWindow", u"ChatGpt", None))
        self.label_user.setText(QCoreApplication.translate("MainWindow", u"User >", None))
        self.pushButton_2.setText("")
    # retranslateUi

