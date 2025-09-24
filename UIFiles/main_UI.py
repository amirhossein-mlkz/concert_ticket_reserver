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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(804, 759)
        icon = QIcon()
        icon.addFile(u":/icons/icons/icons8_cyborg_26px_1.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* ====== GLOBAL THEME (Dark Navy + Gray) ====== */\n"
"QWidget {\n"
"    background-color: #1b2430; /* \u0633\u0631\u0645\u0647\u200c\u0627\u06cc \u062a\u06cc\u0631\u0647 \u0648 \u0645\u062f\u0631\u0646 */\n"
"    font-family: \"Segoe UI\", \"Roboto\", \"Helvetica Neue\", Arial;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: #eaeaea; /* \u062e\u0627\u06a9\u0633\u062a\u0631\u06cc \u0631\u0648\u0634\u0646 \u0628\u0631\u0627\u06cc \u0645\u062a\u0646 */\n"
"}\n"
"\n"
"#info_frame, #bot_info{\n"
"	background-color: rgb(48, 65, 86);\n"
"	padding: 10px;\n"
"}\n"
"\n"
"/* ====== LABEL ====== */\n"
"QLabel {\n"
"    color: #f5f5f5;\n"
"    font-weight: bold;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QLabel[role=\"title\"] {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QLabel[role=\"subtitle\"] {\n"
"    font-size: 13px;\n"
"    color: #b0b8c1;\n"
"}\n"
"\n"
"/* ====== LINE EDIT ====== */\n"
"QLineEdit {\n"
"    border: 1px solid #2f3b52;\n"
""
                        "    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    background-color: #2a3445;\n"
"    color: #f5f5f5;\n"
"    selection-background-color: #00bcd4;\n"
"    selection-color: black;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #3ddcff;\n"
"}\n"
"\n"
"/* ====== SPIN BOX ====== */\n"
"QSpinBox {\n"
"    border: 1px solid #2f3b52;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    background-color: #2a3445;\n"
"    color: #f5f5f5;\n"
"}\n"
"\n"
"/* \u0645\u062e\u0641\u06cc \u06a9\u0631\u062f\u0646 \u062f\u06a9\u0645\u0647\u200c\u0647\u0627\u06cc \u0628\u0627\u0644\u0627/\u067e\u0627\u06cc\u06cc\u0646 */\n"
"QSpinBox::up-button,\n"
"QSpinBox::down-button {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: none;\n"
"    background: none;\n"
"}\n"
"\n"
"/* \u0641\u0648\u06a9\u0648\u0633 */\n"
"QSpinBox:focus {\n"
"    border: 1px solid #3ddcff;\n"
"}\n"
"\n"
"/* ====== COMBO BOX ====== */\n"
"QComboBox {\n"
"    border: 1px solid #2f3b52;\n"
"    border-radius: 8px;\n"
"    padding: "
                        "6px 10px;\n"
"    background-color: #2a3445;\n"
"    color: #f5f5f5;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 24px;\n"
"    background-color: #2a3445;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #3ddcff;\n"
"}\n"
"\n"
"/* ====== BUTTONS ====== */\n"
"QPushButton {\n"
"    background-color: #3ddcff;\n"
"    color: #0d1b2a;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 8px 14px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2fb8d9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2496b3;\n"
"}\n"
"\n"
"/* ====== CHECKBOX ====== */\n"
"QCheckBox {\n"
"    spacing: 8px;\n"
"    color: #eaeaea;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 4px;\n"
"    border: 1px solid #2f3b52;\n"
"    background-color: #2a3445;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #3ddcff;\n"
"    image: url(:/icons/icons/icons8_"
                        "done_26px.png);\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.log_label = QLabel(self.centralwidget)
        self.log_label.setObjectName(u"log_label")
        self.log_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.log_label.setStyleSheet(u"color: rgb(221, 54, 24);")

        self.verticalLayout.addWidget(self.log_label)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.info_frame = QFrame(self.page)
        self.info_frame.setObjectName(u"info_frame")
        self.info_frame.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.info_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 10, 1, 10)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 22, -1, -1)
        self.label = QLabel(self.info_frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.phone_input = QLineEdit(self.info_frame)
        self.phone_input.setObjectName(u"phone_input")
        self.phone_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.gridLayout.addWidget(self.phone_input, 2, 1, 1, 1)

        self.name_input = QLineEdit(self.info_frame)
        self.name_input.setObjectName(u"name_input")

        self.gridLayout.addWidget(self.name_input, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_2 = QLabel(self.info_frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)

        self.label_4 = QLabel(self.info_frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.family_input = QLineEdit(self.info_frame)
        self.family_input.setObjectName(u"family_input")

        self.gridLayout.addWidget(self.family_input, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.verticalSpacer_3 = QSpacerItem(17, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.save_info = QPushButton(self.info_frame)
        self.save_info.setObjectName(u"save_info")
        self.save_info.setMinimumSize(QSize(150, 0))
        self.save_info.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_3.addWidget(self.save_info, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.info_frame)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.bot_info = QFrame(self.page)
        self.bot_info.setObjectName(u"bot_info")
        self.bot_info.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.bot_info)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 22, -1, 24)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.label_10 = QLabel(self.bot_info)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setEnabled(False)

        self.gridLayout_2.addWidget(self.label_10, 3, 5, 1, 1)

        self.label_11 = QLabel(self.bot_info)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setEnabled(False)

        self.gridLayout_2.addWidget(self.label_11, 4, 5, 1, 1)

        self.start_chair = QSpinBox(self.bot_info)
        self.start_chair.setObjectName(u"start_chair")
        self.start_chair.setEnabled(True)
        self.start_chair.setMinimumSize(QSize(150, 0))
        self.start_chair.setMinimum(0)
        self.start_chair.setMaximum(1000)
        self.start_chair.setValue(0)

        self.gridLayout_2.addWidget(self.start_chair, 3, 4, 1, 1)

        self.label_8 = QLabel(self.bot_info)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color:rgb(78, 158, 118);")

        self.gridLayout_2.addWidget(self.label_8, 0, 3, 1, 1)

        self.label_6 = QLabel(self.bot_info)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 1, 5, 1, 1)

        self.label_9 = QLabel(self.bot_info)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"color:rgb(78, 158, 118);")

        self.gridLayout_2.addWidget(self.label_9, 1, 3, 1, 1)

        self.label_7 = QLabel(self.bot_info)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color:red;")

        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)

        self.sans_idx = QSpinBox(self.bot_info)
        self.sans_idx.setObjectName(u"sans_idx")
        self.sans_idx.setMinimumSize(QSize(100, 0))
        self.sans_idx.setMinimum(1)
        self.sans_idx.setMaximum(10)
        self.sans_idx.setValue(1)

        self.gridLayout_2.addWidget(self.sans_idx, 1, 4, 1, 1)

        self.label_5 = QLabel(self.bot_info)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)

        self.gridLayout_2.addWidget(self.label_5, 2, 5, 1, 1)

        self.label_3 = QLabel(self.bot_info)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 5, 1, 1)

        self.reserve_count = QSpinBox(self.bot_info)
        self.reserve_count.setObjectName(u"reserve_count")
        self.reserve_count.setMinimumSize(QSize(100, 0))
        self.reserve_count.setMinimum(1)
        self.reserve_count.setMaximum(10)
        self.reserve_count.setValue(5)

        self.gridLayout_2.addWidget(self.reserve_count, 0, 4, 1, 1)

        self.min_price = QSpinBox(self.bot_info)
        self.min_price.setObjectName(u"min_price")
        self.min_price.setEnabled(False)
        self.min_price.setMinimumSize(QSize(150, 0))
        self.min_price.setMinimum(0)
        self.min_price.setMaximum(10000000)
        self.min_price.setValue(0)

        self.gridLayout_2.addWidget(self.min_price, 2, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.end_chair = QSpinBox(self.bot_info)
        self.end_chair.setObjectName(u"end_chair")
        self.end_chair.setEnabled(True)
        self.end_chair.setMinimumSize(QSize(150, 0))
        self.end_chair.setMinimum(0)
        self.end_chair.setMaximum(1000)
        self.end_chair.setValue(0)

        self.gridLayout_2.addWidget(self.end_chair, 4, 4, 1, 1)

        self.start_chair_checkbox = QCheckBox(self.bot_info)
        self.start_chair_checkbox.setObjectName(u"start_chair_checkbox")

        self.gridLayout_2.addWidget(self.start_chair_checkbox, 3, 6, 1, 1)

        self.end_chair_checkbox = QCheckBox(self.bot_info)
        self.end_chair_checkbox.setObjectName(u"end_chair_checkbox")

        self.gridLayout_2.addWidget(self.end_chair_checkbox, 4, 6, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.input_url = QLineEdit(self.bot_info)
        self.input_url.setObjectName(u"input_url")

        self.verticalLayout_4.addWidget(self.input_url)

        self.verticalSpacer_4 = QSpacerItem(17, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.start_reserve_btn = QPushButton(self.bot_info)
        self.start_reserve_btn.setObjectName(u"start_reserve_btn")
        self.start_reserve_btn.setMinimumSize(QSize(150, 0))
        self.start_reserve_btn.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_4.addWidget(self.start_reserve_btn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_2.addWidget(self.bot_info)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.name_input, self.family_input)
        QWidget.setTabOrder(self.family_input, self.phone_input)
        QWidget.setTabOrder(self.phone_input, self.save_info)
        QWidget.setTabOrder(self.save_info, self.reserve_count)
        QWidget.setTabOrder(self.reserve_count, self.sans_idx)
        QWidget.setTabOrder(self.sans_idx, self.min_price)
        QWidget.setTabOrder(self.min_price, self.start_chair)
        QWidget.setTabOrder(self.start_chair, self.end_chair)
        QWidget.setTabOrder(self.end_chair, self.input_url)
        QWidget.setTabOrder(self.input_url, self.start_reserve_btn)
        QWidget.setTabOrder(self.start_reserve_btn, self.start_chair_checkbox)
        QWidget.setTabOrder(self.start_chair_checkbox, self.end_chair_checkbox)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u06a9\u0646\u0633\u0631\u062a \u0628\u0627\u062a", None))
        self.log_label.setText(QCoreApplication.translate("MainWindow", u"\u0633\u0644\u0627\u0645", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u0631\u0632\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.phone_input.setText("")
        self.phone_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u062e\u0648\u062f \u0631\u0627 \u0648\u0627\u0631\u062f \u06a9\u0646\u06cc\u062f", None))
        self.name_input.setText("")
        self.name_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u062e\u0648\u062f \u0631\u0627 \u0648\u0627\u0631\u062f \u06a9\u0646\u06cc\u062f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u0645\u0648\u0628\u0627\u06cc\u0644 \u0631\u0632\u0631\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u062e\u0627\u0646\u0648\u062f\u0627\u06af\u06cc \u0631\u0632\u0648 \u06a9\u0646\u0646\u062f\u0647", None))
        self.family_input.setText("")
        self.family_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0646\u0627\u0645 \u062e\u0627\u0646\u0648\u0627\u062f\u06af\u06cc \u062e\u0648\u062f \u0631\u0627 \u0648\u0627\u0631\u062f \u06a9\u0646\u06cc\u062f", None))
        self.save_info.setText(QCoreApplication.translate("MainWindow", u"\u0630\u062e\u06cc\u0631\u0647 \u0627\u0637\u0644\u0627\u0639\u0627\u062a", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u0635\u0646\u062f\u0644\u06cc \u0634\u0631\u0648\u0639", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u0635\u0646\u062f\u0644\u06cc \u067e\u0627\u06cc\u0627\u0646\u06cc", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0641\u0639\u0627\u0644", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0634\u0645\u0627\u0631\u0647 \u0633\u0627\u0646\u0633", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u0641\u0639\u0627\u0644", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u063a\u06cc\u0631 \u0641\u0639\u0627\u0644", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u062d\u062f\u0627\u0642\u0644 \u0642\u06cc\u0645\u062a (\u062a\u0648\u0645\u0627\u0646)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u062a\u0639\u062f\u0627\u062f \u0631\u0632\u0631\u0648", None))
        self.start_chair_checkbox.setText("")
        self.end_chair_checkbox.setText("")
        self.input_url.setText("")
        self.input_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0622\u062f\u0631\u0633 \u06a9\u0646\u0633\u0631\u062a \u0645\u0648\u0631\u062f \u0646\u0638\u0631 \u0631\u0627 \u0648\u0627\u0631\u062f \u06a9\u0646\u06cc\u062f", None))
        self.start_reserve_btn.setText(QCoreApplication.translate("MainWindow", u"\u0631\u0632\u0631\u0648", None))
    # retranslateUi

