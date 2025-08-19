# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_UI.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"*{\n"
"font-size: 14px;\n"
"}\n"
"QPushButton{\n"
"	min-height:30px;\n"
"	border-radius: 14px;\n"
"	background-color:rgb(85, 170, 127);\n"
"	font-weight:bold;\n"
"	color: #fff;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(54, 109, 81);\n"
"}\n"
"\n"
"\n"
"QLineEdit{\n"
"	min-height: 30px;\n"
"	border: 0px solid rgb(85, 170, 127);\n"
"	border-bottom: 2px solid rgb(85, 170, 127);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"        border-bottom: 2px solid rgb(54, 109, 81);\n"
"    }\n"
"\n"
"QLabel{\n"
"	font-weight:bold;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.log_label = QLabel(self.centralwidget)
        self.log_label.setObjectName(u"log_label")
        self.log_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.log_label.setStyleSheet(u"color: rgb(221, 54, 24);")

        self.verticalLayout.addWidget(self.log_label)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 22, -1, -1)
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.phone_input = QLineEdit(self.page)
        self.phone_input.setObjectName(u"phone_input")
        self.phone_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.gridLayout.addWidget(self.phone_input, 2, 1, 1, 1)

        self.name_input = QLineEdit(self.page)
        self.name_input.setObjectName(u"name_input")

        self.gridLayout.addWidget(self.name_input, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)

        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.family_input = QLineEdit(self.page)
        self.family_input.setObjectName(u"family_input")

        self.gridLayout.addWidget(self.family_input, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.save_info = QPushButton(self.page)
        self.save_info.setObjectName(u"save_info")
        self.save_info.setMinimumSize(QSize(150, 30))
        self.save_info.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_2.addWidget(self.save_info, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.reserve_count = QSpinBox(self.page)
        self.reserve_count.setObjectName(u"reserve_count")
        self.reserve_count.setMinimumSize(QSize(100, 0))
        self.reserve_count.setMinimum(1)
        self.reserve_count.setMaximum(10)
        self.reserve_count.setValue(5)

        self.gridLayout_2.addWidget(self.reserve_count, 0, 3, 1, 1)

        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 4, 1, 1)

        self.label_5 = QLabel(self.page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)

        self.gridLayout_2.addWidget(self.label_5, 1, 4, 1, 1)

        self.min_price = QSpinBox(self.page)
        self.min_price.setObjectName(u"min_price")
        self.min_price.setEnabled(False)
        self.min_price.setMinimumSize(QSize(150, 0))
        self.min_price.setMinimum(0)
        self.min_price.setMaximum(10000000)
        self.min_price.setValue(0)

        self.gridLayout_2.addWidget(self.min_price, 1, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.input_url = QLineEdit(self.page)
        self.input_url.setObjectName(u"input_url")

        self.horizontalLayout.addWidget(self.input_url)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.start_reserve_btn = QPushButton(self.page)
        self.start_reserve_btn.setObjectName(u"start_reserve_btn")
        self.start_reserve_btn.setMinimumSize(QSize(150, 30))

        self.horizontalLayout_2.addWidget(self.start_reserve_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.log_label.setText(QCoreApplication.translate("MainWindow", u"\u0633\u0644\u0627\u0645", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u0631\u0632\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.phone_input.setText(QCoreApplication.translate("MainWindow", u"09136563912", None))
        self.name_input.setText(QCoreApplication.translate("MainWindow", u"\u0627\u0645\u06cc\u0631", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u0645\u0648\u0628\u0627\u06cc\u0644 \u0631\u0632\u0631\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u062e\u0627\u0646\u0648\u062f\u0627\u06af\u06cc \u0631\u0632\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.family_input.setText(QCoreApplication.translate("MainWindow", u"\u0627\u0645\u06cc\u0631", None))
        self.save_info.setText(QCoreApplication.translate("MainWindow", u"\u0630\u062e\u06cc\u0631\u0647 \u0627\u0637\u0644\u0627\u0639\u0627\u062a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u062a\u0639\u062f\u0627\u062f \u0631\u0632\u0631\u0648", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u062d\u062f\u0627\u0642\u0644 \u0642\u06cc\u0645\u062a (\u062a\u0648\u0645\u0627\u0646)", None))
        self.input_url.setText(QCoreApplication.translate("MainWindow", u"https://www.melotik.com/event/14", None))
        self.start_reserve_btn.setText(QCoreApplication.translate("MainWindow", u"\u0631\u0632\u0631\u0648", None))
    # retranslateUi

