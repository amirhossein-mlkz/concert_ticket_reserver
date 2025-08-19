import time
from datetime import datetime, date

import re
import numpy as np
from PySide6.QtWidgets import QApplication, QToolButton
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from UIFiles.defect_notification import Ui_Notification
from UIFiles.progress_dialog import Ui_progressDialog
from UIFiles.verify_UI import Ui_verifyDialogWin
from UIFiles.calendar import Ui_CalendarDialog
from backend.UserManager.userLoginRegister import passwordManager
from uiUtils.guiBackend import GUIBackend
from Constants import Constant
from Constants import Constant
from Constants import IconsPath

CODE_NAME_BUTTON_STYLE = {
    'normal': """ QPushButton{
                  min-width:100px;
                  background-color: rgb(150,150,150);
                }


            QPushButton:hover{
            background-color: rgb(50,50,50);
            }
            """,

    'active':
            """ QPushButton{
                  min-width:100px;
                  background-color: rgb(58, 209, 154);
                }


            QPushButton:hover{
            background-color: rgb(58, 209, 154);
            }
            """

}

TABEL_BUTTON_STYLE = """
    QPushButton{ 
        background-color: rgba(255,255,255,0);
        border: 0px solid gray;
        min-height:0px; min-width:0px; 
        width:auto;
        } 
    """

SIDEBAR_BUTTON_SELECTED_STYLE = """
    QPushButton{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #4C7EFF, stop: 0.029 #4C7EFF, stop: 0.03 rgba(120, 146, 223, 40), stop: 1 rgba(120, 146, 223, 40));
        }

"""

SIDEBAR_BUTTON_UNSELECTED_STYLE = """
    None

"""

MULTISTEP_SELECT_STYLE = """
    QPushButton{
        background-color: transparent;
        border:5px solid #4C7EFF;
        border-radius: 32px;
        min-width: 55px;
        max-width: 55px;
        min-height: 55px;
        max-height: 55px;
        font-size: 24px;
        color: rgb(20, 20, 20);
        font-weight: bold;
    }

    QPushButton:hover{
        border:5px solid #83A5FC;
    }
"""

MULTISTEP_UNSELECT_STYLE = """
    QPushButton{
        background-color: transparent;
        border:5px solid #7E84A2;
        border-radius: 32px;
        min-width: 55px;
        max-width: 55px;
        min-height: 55px;
        max-height: 55px;
        font-size: 24px;
        color: rgb(20, 20, 20);
        font-weight: bold;
    }

    QPushButton:hover{
        border:5px solid #BDBDBF;
    }
"""

REPORT_BUTTON_STYLE = """
QPushButton{
	min-height:30px;
    min-width:30px;
    max-height:30px;
    max-width:30px;
	border-radius:3px;
	color: rgb(255, 255, 255);
	background-color:rgb(54, 193, 142);

}

QPushButton:hover{
	color: rgb(255, 255, 255);
	background-color:rgb(40, 144, 106);
}

"""

TABLE_BUTTON_STYLE = """
QPushButton{
	min-height:30px;
    min-width:100px;
    max-height:30px;
    max-width:100px;
	border-radius:3px;
	color: rgb(255, 255, 255);
	background-color:rgb(54, 193, 142);

}

QPushButton:hover{
	color: rgb(255, 255, 255);
	background-color:rgb(40, 144, 106);
}
"""

CONFIRMBOX_STYLESHEET = """
QMessageBox{ 
    background-color: #a6acb3;
    font: auto "Roboto";
    font-size: 16px;
}

QMessageBox QLabel#qt_msgbox_label {
    min-width: 400px;
}

QMessageBox QLabel#qt_msgbox_label {
    min-width: 400px;
}
"""

OK_BUTTUN_STYLE= """
QPushButton
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(46, 76, 153, 255), stop:1 rgba(76, 126, 255, 255));
    color: rgba(255, 255, 255, 210);
    border-radius: 20px;
    min-width: 100;
    max-width: 100;
    min-height: 40;
    max-height: 40;
    font-size: 14px;
    font-weight: bold;
    icon: url({0})
}}

QPushButton:hover
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(77, 98, 153, 255), stop:1 rgba(114, 152, 252, 255));
}}

QPushButton:pressed
{{
    padding-left: 5px;
    padding-top: 5px;
}}
""".format(IconsPath.IconsPath.TICK_PATH)

YES_BUTTUN_STYLE= """
QPushButton
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(46, 76, 153, 255), stop:1 rgba(76, 126, 255, 255));
    color: rgba(255, 255, 255, 210);
    border-radius: 20px;
    min-width: 100;
    max-width: 100;
    min-height: 40;
    max-height: 40;
    font-size: 14px;
    font-weight: bold;
    icon: url({0})
}}

QPushButton:hover
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(77, 98, 153, 255), stop:1 rgba(114, 152, 252, 255));
}}

QPushButton:pressed
{{
    padding-left: 5px;
    padding-top: 5px;
}}
""".format(IconsPath.IconsPath.TICK_PATH)

SAVE_BUTTUN_STYLE= """
QPushButton
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(46, 76, 153, 255), stop:1 rgba(76, 126, 255, 255));
    color: rgba(255, 255, 255, 210);
    border-radius: 20px;
    min-width: 100;
    max-width: 100;
    min-height: 40;
    max-height: 40;
    font-size: 14px;
    font-weight: bold;
    icon: url({0})
}}

QPushButton:hover
{{
    background-color: qlineargradient(spread:pad, x1:0.635, y1:1, x2:0.44, y2:0, stop:0 rgba(77, 98, 153, 255), stop:1 rgba(114, 152, 252, 255));
}}

QPushButton:pressed
{{
    padding-left: 5px;
    padding-top: 5px;
}}
""".format(IconsPath.IconsPath.SAVE_PATH)

CANCEL_BUTTUN_STYLE= """
QPushButton
{{
    border: 2px solid  rgba(46, 76, 153, 255);
    color:  rgba(46, 76, 153, 255);
    border-radius: 18px;
    min-width: 100;
    max-width: 100;
    min-height: 36;
    max-height: 36;
    font-size: 14px;
    font-weight: bold;
    icon: url({0});
}}

QPushButton:hover
{{
    border: 2px solid rgba(76, 126, 255, 255);
    color:  rgba(76, 126, 255, 255);
    icon: url({1});
}}

QPushButton:pressed
{{
    padding-left: 5px;
    padding-top: 5px;
}}
""".format(IconsPath.IconsPath.CANCEL_PATH, IconsPath.IconsPath.CANCEL_HOVER_PATH)

NO_BUTTUN_STYLE= """
QPushButton
{{
    border: 2px solid  rgba(46, 76, 153, 255);
    color:  rgba(46, 76, 153, 255);
    border-radius: 18px;
    min-width: 100;
    max-width: 100;
    min-height: 36;
    max-height: 36;
    font-size: 14px;
    font-weight: bold;
    icon: url({0});
}}

QPushButton:hover
{{
    border: 2px solid rgba(76, 126, 255, 255);
    color:  rgba(76, 126, 255, 255);
    icon: url({1});
}}

QPushButton:pressed
{{
    padding-left: 5px;
    padding-top: 5px;
}}
""".format(IconsPath.IconsPath.CANCEL_PATH, IconsPath.IconsPath.CANCEL_HOVER_PATH)

IGNORE_BUTTUN_STYLE= """
QPushButton
{
    border: 2px solid  rgba(46, 76, 153, 255);
    color:  rgba(46, 76, 153, 255);
    border-radius: 18px;
    min-width: 100;
    max-width: 100;
    min-height: 36;
    max-height: 36;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover
{
    border: 2px solid rgba(76, 126, 255, 255);
    color:  rgba(76, 126, 255, 255);
}

QPushButton:pressed
{
    padding-left: 5px;
    padding-top: 5px;
}
"""

COMPARE_COMBOBOXE = """
                    QComboBox
{
	border:2px solid rgb(6, 76, 130);
    border-radius: 1px;
    padding: 3px;
	min-width:0xp;
	min-height: 0px;
    max-height: 18px;
	font-size: 14px;
}

QComboBox:enabled{
color: rgb(50, 50, 50);
}

QComboBox::down-arrow
{   
	image: url(:/assets/icons/icons8-downtriangle-48.png);
	width: 8px;
    height: 8px;
     background-color: rgb(6, 76, 130);
	 min-width: 0px;
     max-height: 17px;

}
        """

TABLE_SPINBOX = """
QSpinBox, QDoubleSpinBox  
{
	border:2px solid rgb(6, 76, 130);
    border-radius: 3px;
    padding: 2px;
    min-width:0xp;
	min-height: 0px;
    max-height: 20px;
	font-size: 12px;
}

QSpinBox:enabled, QDoubleSpinBox:enabled{
color: rgb(50, 50, 50);
}


QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QSpinBox::down-arrow ,  QDoubleSpinBox::down-arrow
{   
	image: url(noimg);
	width: 0px;
    height: 0px;

}


QSpinBox::up-button,
QSpinBox::down-button,
QDoubleSpinBox::up-button,
QDoubleSpinBox::down-button   {
    subcontrol-origin: border;
	background-color:rgb(6, 76, 130);
    width: 0px;
}


QSpinBox::up-button:disabled ,
QSpinBox::down-button:disabled ,
QDoubleSpinBox::up-button:disabled ,
QDoubleSpinBox::down-button:disabled    {
    subcontrol-origin: border;
    background-color:rgb(209, 209, 209);
    width: 0px;
}

QSpinBox:focus, QDoubleSpinBox:focus{
    background: rgb(241, 241, 241);
    /*selection-background-color: black;*/
}

"""


def take_closest(num, collection):
    return min(collection, key=lambda x: abs(x - num))


def single_timer_runner( t, func):
    """runs a function after a delay time

    Args:
        t (_type_): delay time in ms`
        func (_type_): function event after time finished
    """
    timer = QtCore.QTimer()
    timer.singleShot(t, func)

class Calendar(QtWidgets.QDialog):
    def __init__(self, input_field:QtWidgets.QDateEdit) -> None:
        super(Calendar, self).__init__()

        self.ui = Ui_CalendarDialog()
        self.ui.setupUi(self)
        self.input_field = input_field

        GUIBackend.set_win_frameless(self)
        GUIBackend.set_win_attribute(self, QtCore.Qt.WA_TranslucentBackground)

        GUIBackend.button_connector(self.ui.cancel_btn, self.close_win)
        GUIBackend.button_connector(self.ui.ok_btn, self.__update__date_field)

        self.move_refresh_time = 0
        self.offset = None

        self.selected_date = None

        self._center()
        self._styler()

    def _center(self):
        primary_screen = QApplication.primaryScreen()

        if primary_screen:
            screen_geometry = primary_screen.geometry()

            center_point = screen_geometry.center()

            self.move(center_point.x() - self.frameGeometry().width() // 2,
                      center_point.y() - self.frameGeometry().height() // 2)
            
    def _styler(self):
        self._style_next_prev()
        self._style_today()
            
    def _style_next_prev(self):
        prev_month_button = self.ui.calendar.findChild(QToolButton, 'qt_calendar_prevmonth')
        next_month_button = self.ui.calendar.findChild(QToolButton, 'qt_calendar_nextmonth')

        prev_month_button.setIcon(QtGui.QIcon(':/icons/icons/prev_gray.png'))
        next_month_button.setIcon(QtGui.QIcon(':/icons/icons/next_gray.png'))

        prev_month_button.setCursor(QtGui.QCursor(QtGui.Qt.PointingHandCursor))
        next_month_button.setCursor(QtGui.QCursor(QtGui.Qt.PointingHandCursor))

    def _style_today(self):
        today_format = QtGui.QTextCharFormat()
        today_format.setForeground(QtGui.QColor('#4C7EFF'))

        self.ui.calendar.setDateTextFormat(QtCore.QDate.currentDate(), today_format)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = QtCore.QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            if time.time() - self.move_refresh_time > Constant.RefreshRates.MOUSE_MOVE:
                self.move_refresh_time = time.time()
                self.move(self.pos() + QtCore.QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def show_win(self):
        date = GUIBackend.get_date_input(self.input_field)
        self.__set_date(date)
    
        GUIBackend.show_window(self, always_on_top=True)

    def close_win(self):
        GUIBackend.close_window(self)

    def __update__date_field(self):
        selected_date = self.ui.calendar.selectedDate().toPython()
        GUIBackend.set_date_input(self.input_field, selected_date)
        self.close_win()
    
    def __set_date(self, date:datetime):
        date = QtCore.QDate(date.year, date.month, date.day)
        self.ui.calendar.setSelectedDate(date)


class VerifyUser(QtWidgets.QDialog):
    def __init__(self, username, password) -> None:
        super(VerifyUser, self).__init__()

        self.ui = Ui_verifyDialogWin()
        self.ui.setupUi(self)

        GUIBackend.set_input_password(self.ui.verify_password_input)
        GUIBackend.set_win_frameless(self)
        GUIBackend.set_win_attribute(self, QtCore.Qt.WA_TranslucentBackground)
        GUIBackend.button_connector(self.ui.close_btn, self.close_win)
        GUIBackend.button_connector(self.ui.verify_eye_btn, self.show_hide_password)
        GUIBackend.button_connector(self.ui.verify_btn, self.verify_password)

        self.username = username
        self.password = password

        self.move_refresh_time = 0
        self.show_password = False

        self.offset = None

        self._center()

        self.set_verification_message()

    def _center(self):
        # Get primary screen
        primary_screen = QApplication.primaryScreen()

        if primary_screen:
            # Get geometry of the primary screen
            screen_geometry = primary_screen.geometry()

            # Calculate center point
            center_point = screen_geometry.center()

            # Set window position to be centered
            self.move(center_point.x() - self.frameGeometry().width() // 2,
                      center_point.y() - self.frameGeometry().height() // 2)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and event.y() < self.ui.top_frame.height():
            self.offset = QtCore.QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            if time.time() - self.move_refresh_time > Constant.RefreshRates.MOUSE_MOVE:
                self.move_refresh_time = time.time()
                self.move(self.pos() + QtCore.QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Enter key
            self.ui.verify_btn.click()

    def set_verification_message(self):
        GUIBackend.set_label_text(self.ui.verify_message, 'Enter {} Password'.format(self.username))

    def verify_password(self):
        enterd_password = self.get_inputs()
        if passwordManager.check_password(Constant.User.UNLOGIN_USER_PASSWORD, self.password):
            self.write_error('Password is Wrong')
        res = passwordManager.check_password(enterd_password, self.password)
        if not res:
            self.write_error('Password is Wrong')
        else:
            self.accept()

    def render(self):
        self.write_error(None)
        return self.exec_()

    def close_win(self):
        self.clear_inputs()
        GUIBackend.close_window(self)
        self.reject()

    def show_hide_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            GUIBackend.set_input_normal(self.ui.verify_password_input)
            GUIBackend.set_button_icon(self.ui.verify_eye_btn, IconsPath.IconsPath.WHITE_HIDE_PASSWORD)
        else:
            GUIBackend.set_input_password(self.ui.verify_password_input)
            GUIBackend.set_button_icon(self.ui.verify_eye_btn, IconsPath.IconsPath.WHITE_SHOW_PASSWORD)

    def get_inputs(self):
        password = GUIBackend.get_input(self.ui.verify_password_input)
        return password

    def clear_inputs(self):
        GUIBackend.set_input(self.ui.verify_password_input, "")

    def write_error(self, txt:str):
        """Write Errors message in Logun

        Args:
            txt (str): error message
        """
        if txt is None:
            GUIBackend.set_wgt_visible(self.ui.verify_error_lbl, False)
        else:
            GUIBackend.set_wgt_visible(self.ui.verify_error_lbl, True)
            GUIBackend.set_label_text( self.ui.verify_error_lbl, txt)


class PhotoViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent=None, min_scale=1/3, max_scale=3):
        super().__init__(parent)

        # Set up the scene and the view
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.min_scale = min_scale
        self.max_scale = max_scale


        # Keep track of the current image
        self.pixmap_item = None

        self.zoom_factor = 1.25
        self.current_scale = 1

        # Enable mouse interaction for zoom and panning
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    
    def set_scale_range(self, min_scale, max_scale):
        self.min_scale = min_scale
        self.max_scale = max_scale

    def set_image(self, image_array: np.ndarray):
        """ Load an image from a NumPy array """

        # Convert NumPy array to QImage
        if len(image_array.shape) == 2:  # Grayscale image
            height, width = image_array.shape
            qimage = QtGui.QImage(image_array.data, width, height, QtGui.QImage.Format_Grayscale8)
        elif len(image_array.shape) == 3 and image_array.shape[2] == 3:  # RGB image
            height, width, channels = image_array.shape
            qimage = QtGui.QImage(image_array.data, width, height, channels * width, QtGui.QImage.Format_RGB888)
        elif len(image_array.shape) == 3 and image_array.shape[2] == 4:  # RGBA image
            height, width, channels = image_array.shape
            qimage = QtGui.QImage(image_array.data, width, height, channels * width, QtGui.QImage.Format_RGBA8888)
        else:
            print("Unsupported NumPy array format")
            return

        # Remove the old image if any
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)

        # Create a pixmap from the QImage and add it to the scene
        pixmap = QtGui.QPixmap.fromImage(qimage)
        self.pixmap_item = self.scene.addPixmap(pixmap)

        # Resize the view to fit the image
        self.setSceneRect(self.pixmap_item.boundingRect())

        # Fit the image in the view, keeping the aspect ratio
        if self.current_scale == 1:
            self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)

    def clear(self):
        """ Clear the current image from the view """
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)
            self.pixmap_item = None
            self.scene.clear()

    def wheelEvent(self, event):
        """ Override the wheel event to implement zoom functionality """
        if event.angleDelta().y() > 0:
            
            if self.current_scale*self.zoom_factor <= self.max_scale:
                self.scale(self.zoom_factor, self.zoom_factor)
                self.current_scale *= self.zoom_factor 
        else:
            if self.current_scale/self.zoom_factor >= self.min_scale:
                self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
                self.current_scale /= self.zoom_factor

class Color:
    def __init__(self, color) -> None:
        if self.is_hex_color(color):
            self.hex_color = color
            self.rgb_color = self.hex2rgb(color)

        elif self.is_rgb_color(color):
            self.hex_color = self.rgb2hex(color)
            self.rgb_color = tuple(map(int, color.strip('()').split(', ')))

        else:
            raise "{color} is not a valid Hex or RGB color."

    def is_hex_color(self, color):
        """
        Check if the given color is a valid hexadecimal color code.
        """
        hex_color_pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        return re.match(hex_color_pattern, color) is not None

    def is_rgb_color(self, color):
        """
        Check if the given color is a valid RGB color in the format (x, y, z).
        """
        rgb_color_pattern = r'^\(\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\s*\)$'
        match = re.match(rgb_color_pattern, color)
        if match:
            r, g, b = map(int, match.groups())
            return all(0 <= val <= 255 for val in [r, g, b])
        return False
        
    def rgb2hex(self, color):
        """
        Convert RGB to Hexadecimal color code.
        """
        if self.is_rgb_color(color):
            r, g, b = map(int, color.strip('()').split(', '))
            return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
        else:
            raise ValueError("Invalid RGB color format")

    def hex2rgb(self, color):
        """
        Convert Hexadecimal color code to RGB.
        """
        if self.is_hex_color(color):
            hexcolor = color.lstrip('#')
            if len(hexcolor) == 6:
                r, g, b = tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4))
            elif len(hexcolor) == 3:
                r, g, b = tuple(int(hexcolor[i:i+1]*2, 16) for i in (0, 1, 2))
            else:
                raise ValueError("Invalid hex color format")
            return r, g, b
        else:
            raise ValueError("Invalid hex color format")


class AnimatedTextEdit(QtWidgets.QTextEdit):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

    def fade_in(self, duration=1000, callback=None):
        self.__fade(0.0, 1.0, duration, callback)

    def fade_out(self, duration=1000, callback=None):
        self.__fade(1.0, 0.0, duration,callback)

    def __fade(self, start_opacity, end_opacity, duration, callback=None):
        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(start_opacity)
        self.animation.setEndValue(end_opacity)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.animation.finished.connect(callback)
        self.animation.start()


class Message(AnimatedTextEdit):
    def __init__(self, parent, title:str, text:str, color:tuple, icon_path:str):
        super().__init__(text, parent)
        self.setEnabled(False)
        parent.layout().insertWidget(0, self)

        self.style = (
            """QTextEdit
            {{
                color: rgb(20, 20, 20);
                border: None;
                border-bottom: 2px solid rgba({0}, {1}, {2}, 255);
                background-color: rgba({0}, {1}, {2}, 50);
                padding-left: 55px;
                padding-top: 6px;
                padding-bottom: 3x;
                background-image: url({3});
                background-position: left center;
                background-repeat: no-repeat;
                min-height: 65px;
                max-height: 65px;
            }}

            QTextEdit:disabled
            {{
                color: rgb(20, 20, 20)
            }}"""

        )

        self.style = self.style.replace('\n', '').replace('\t', '')

        self.set_style(color, icon_path)

        self.html_text = (
                """<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600; color:{};">{}</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{}</p></body></html>"""
            )
        
        self.set_message(title, text, color)

    def set_message(self, title:str, text:str, color:tuple):
        color_obj = Color(color)
        self.setHtml(self.html_text.format(color_obj.hex_color, title, text))

    def set_style(self, color, icon_path):
        color_obj = Color(color)
        self.setStyleSheet(
            self.style.format(color_obj.rgb_color[0], color_obj.rgb_color[1], color_obj.rgb_color[2], icon_path)
        )

    def show_message(self, disappear: bool=True):
        self.fade_in(duration=Constant.MessagesAnimation.FADE_IN_DURATION)

        if disappear:
            single_timer_runner(Constant.MessagesAnimation.MESSAGE_DURARTION, 
                                            lambda: self.fade_out(duration=Constant.MessagesAnimation.FADE_OUT_DURATION, callback=self.deleteLater)
            )

    def hide_message(self):
        self.fade_out(duration=Constant.MessagesAnimation.FADE_OUT_DURATION, callback=self.deleteLater)


class SuccessMessage(Message):
    def __init__(self, parent, text=""):
        title = "SUCCESS"
        color = Constant.MessageColors.SUCCESS
        icon_path = IconsPath.IconsPath.SUCCESS_ICON
        super().__init__(parent, title, text, color, icon_path)


class WarningMessage(Message):
    def __init__(self, parent, text=""):
        title = "WARNING"
        color = Constant.MessageColors.WARNING
        icon_path = IconsPath.IconsPath.WARNING_ICON
        super().__init__(parent, title, text, color, icon_path)


class ErrorMessage(Message):
    def __init__(self, parent, text=""):
        title = "ERROR"
        color = Constant.MessageColors.ERROR
        icon_path = IconsPath.IconsPath.ERROR_ICON
        super().__init__(parent, title, text, color, icon_path)


class InfoMessage(Message):
    def __init__(self, parent, text=""):
        title = "INFO"
        color = Constant.MessageColors.INFO
        icon_path = IconsPath.IconsPath.INFO_PATH
        super().__init__(parent, title, text, color, icon_path)


class TableMessages:
    TABLE_HEADERS = ['icon', 'message', 'delete']
    TABLE_COLUMN_WIDTH = [30, 180, 30]

    def __init__(self, table: QtWidgets.QTableWidget) -> None:
        self.table = table

        self.table.contextMenuEvent = self.context_menu_event_creator()

        GUIBackend.clear_table(self.table)
        
        GUIBackend.set_table_cheaders_visibality(self.table, False)
        GUIBackend.set_table_rheaders_visibality(self.table, False)

        GUIBackend.set_table_dim(self.table, 0, len(self.TABLE_HEADERS))
        GUIBackend.set_table_cheaders(
            self.table, 
            self.TABLE_HEADERS
        )

        for c, width in enumerate(self.TABLE_COLUMN_WIDTH):
            GUIBackend.set_table_cwidth(self.table, c, width)

        self.__strech_message_column()

    def __strech_message_column(self):
        self.table.horizontalHeader().setStretchLastSection(False)
        
        # Set the resize mode for the remaining columns to resize to contents
        for col in range(0, self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)

        # Set the resize mode for the first column to stretch
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


    def add_message(self, message_txt: str, level: int=Constant.MessageLevels.INFO):
        if level==Constant.MessageLevels.INFO:
            icon_path = IconsPath.IconsPath.INFO_PATH
        if level==Constant.MessageLevels.SUCCESS:
            icon_path = IconsPath.IconsPath.SUCCESS_ICON
        if level==Constant.MessageLevels.ERROR:
            icon_path = IconsPath.IconsPath.ERROR_ICON
        if level==Constant.MessageLevels.WARNING:
            icon_path = IconsPath.IconsPath.WARNING_ICON

        GUIBackend.add_table_row(self.table, row_position=0)

        row = 1

        icon_btn = iconButton(icon_normal_path=icon_path)
        GUIBackend.set_table_cell_widget(self.table, (row-1, 0), icon_btn)

        GUIBackend.set_table_cell_value(self.table, (row-1, 1), message_txt, align=False)

        delete_btn = closeButton()
        GUIBackend.set_table_cell_widget(self.table, (row-1, 2), delete_btn)
        delete_btn.clicked.connect(lambda: self.delete_message(delete_btn.pos()))

    def delete_message(self, pos):
        row = self.table.indexAt(pos).row()
        GUIBackend.delete_table_row(self.table, row)

    def delete_all_messages(self):
        GUIBackend.clear_table(self.table)

    def context_menu_event_creator(self):
        def func(event):
            context_menu = QtWidgets.QMenu(self.table)
            clear_action = context_menu.addAction("Clear All")
            clear_action.triggered.connect(self.delete_all_messages)
            context_menu.exec_(event.globalPos())
        return func


class SwitchCircle(QtWidgets.QWidget):
    def __init__(self, parent, dim: int, move_range: tuple, color, animation_curve, animation_duration):
        super().__init__(parent=parent)
        self.color = color
        self.dim = dim
        self.move_range = move_range
        self.animation = QtCore.QPropertyAnimation(self, b"pos")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(animation_duration)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(self.color))
        painter.drawEllipse(0, 0, self.dim, self.dim)
        painter.end()

    def set_color(self, value):
        self.color = value
        self.update()

    def mousePressEvent(self, event):
        self.animation.stop()
        self.oldX = event.globalX()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        delta = event.globalX() - self.oldX
        self.new_x = delta + self.x()
        if self.new_x < self.move_range[0]:
            self.new_x += (self.move_range[0] - self.new_x)
        if self.new_x > self.move_range[1]:
            self.new_x -= (self.new_x - self.move_range[1])
        self.move(self.new_x, self.y())
        self.oldX = event.globalX()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        try:
            go_to = take_closest(self.new_x, self.move_range)
            if go_to == self.move_range[0]:
                self.animation.setStartValue(self.pos())
                self.animation.setEndValue(QtCore.QPoint(go_to, self.y()))
                self.animation.start()
                # self.parent().setChecked(False)
            elif go_to == self.move_range[1]:
                self.animation.setStartValue(self.pos())
                self.animation.setEndValue(QtCore.QPoint(go_to, self.y()))
                self.animation.start()
                # self.parent().setChecked(True)
        except AttributeError:
            pass
        return super().mouseReleaseEvent(event)

class SwitchControl(QtWidgets.QCheckBox):
    def __init__(self, parent=None, bg_color="#BF0000", circle_color="#E0E4EC", active_color="#00BF40",
                 animation_curve=QtCore.QEasingCurve.OutBounce, animation_duration=500, checked: bool = False,
                 change_cursor=True):
        if parent is None:
            super().__init__()
        else:
            super().__init__(parent=parent)

        self.fix_size = (60, 28)
        self.setFixedSize(*self.fix_size)
        if change_cursor:
            self.setCursor(QtCore.Qt.PointingHandCursor)
        self.bg_color = bg_color
        self.circle_color = circle_color
        self.animation_curve = animation_curve
        self.animation_duration = animation_duration
        self.__circle = SwitchCircle(self, int(self.fix_size[1]*0.75), (3, self.width() - int(self.fix_size[1]*0.92)), self.circle_color, self.animation_curve,
                                     self.animation_duration)
        self.__circle_position = 3
        self.active_color = active_color
        self.auto = False
        self.pos_on_press = None
        self.setChecked(checked)
        self.animation = QtCore.QPropertyAnimation(self.__circle, b"pos")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(animation_duration)
        self.disabled_bg_color = "#BDBDBF"
        self.disabled_circle_color = "#D7D7D9"

    def get_bg_color(self):
        return self.bg_color
    
    def change_size(self, size=1):
        if size==1:
            self.fix_size = (45, 18)
        elif size==2:
            self.fix_size = (60, 28)

        self.setFixedSize(*self.fix_size)
        self.__circle.deleteLater()
        self.__circle = None
        self.__circle = SwitchCircle(self, int(self.fix_size[1]*0.75), (3, self.width() - int(self.fix_size[1]*0.92)), self.circle_color, self.animation_curve,
                                     self.animation_duration)
        self.animation = QtCore.QPropertyAnimation(self.__circle, b"pos")
        self.animation.setEasingCurve(self.animation_curve)
        self.animation.setDuration(self.animation_duration)
        
        checked = self.isChecked()
        self.setChecked(checked)
    
    def setChecked(self, state):
        if state:
            self.__circle.move(self.width() - int(self.fix_size[1]*0.92), 3)
            super().setChecked(True)
        elif not state:
            self.__circle.move(3, 3)
            super().setChecked(False)

    @QtCore.Slot(str)
    def set_bg_color(self, value):
        self.bg_color = value
        self.update()

    backgroundColor = QtCore.Property(str, get_bg_color, set_bg_color)

    def get_circle_color(self):
        return self.circle_color

    @QtCore.Slot(str)
    def set_circle_color(self, value):
        self.circle_color = value
        self.__circle.set_color(self.circle_color)
        self.update()

    circleBackgroundColor = QtCore.Property(str, get_circle_color, set_circle_color)

    def get_animation_duration(self):
        return self.animation_duration

    @QtCore.Slot(int)
    def set_animation_duration(self, value):
        self.animation_duration = value
        self.animation.setDuration(value)

    animationDuration = QtCore.Property(int, get_animation_duration, set_animation_duration)

    def get_active_color(self):
        return self.active_color

    @QtCore.Slot(str)
    def set_active_color(self, value):
        self.active_color = value
        self.update()

    activeColor = QtCore.Property(str, get_active_color, set_active_color)

    def start_animation(self, checked):
        self.animation.stop()
        self.animation.setStartValue(self.__circle.pos())
        if checked:
            self.animation.setEndValue(QtCore.QPoint(self.width() - int(self.fix_size[1]*0.92), self.__circle.y()))
            self.setChecked(True)
        if not checked:
            self.animation.setEndValue(QtCore.QPoint(3, self.__circle.y()))
            self.setChecked(False)
        self.animation.start()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        if not self.isEnabled():
            painter.setBrush(QtGui.QColor(self.disabled_bg_color))
        elif not self.isChecked():
            painter.setBrush(QtGui.QColor(self.bg_color))
        else:
            painter.setBrush(QtGui.QColor(self.active_color))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def mousePressEvent(self, event):
        self.auto = True
        self.pos_on_press = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.globalPos() != self.pos_on_press:
            self.auto = False
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.auto:
            self.auto = False
            self.start_animation(not self.isChecked())

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        if enabled:
            self.__circle.set_color(self.circle_color)
        else:
            self.__circle.set_color(self.disabled_circle_color)
        self.update()


class LightIndicator(QtWidgets.QLabel):
    MAIN_STYLESHEET = (
        """QLabel
        {{
            background-color: {0};
            border: 1px solid {0};
            border-radius: {1}px;
            min-width: {2};
            max-width: {2};
            min-height: {2};
            max-height: {2};
        }}"""
    )

    MAIN_STYLESHEET = MAIN_STYLESHEET.replace('\n', '').replace('\t', '')

    def __init__(
            self, 
            parent=None, 
            on_color: Color=Color("#0C8847"), 
            off_color: Color=Color("#EF414D"), 
            unknown_color: Color=Color("#BDBDBF"), 
            radius: int=15
        ):

        if parent is None:
            super().__init__()
        else:
            super().__init__(parent=parent)

        self.on_color = on_color
        self.off_color = off_color
        self.unknown_color = unknown_color
        self.radius = radius

        self.status = -1

    def set_unknown(self):
        self.setStyleSheet(self.MAIN_STYLESHEET.format(self.unknown_color.hex_color, self.radius, self.radius*2))

    def set_off(self):
        self.status = 0
        self.setStyleSheet(self.MAIN_STYLESHEET.format(self.off_color.hex_color, self.radius, self.radius*2))

    def set_on(self):
        self.status = 1
        self.setStyleSheet(self.MAIN_STYLESHEET.format(self.on_color.hex_color, self.radius, self.radius*2))

    def get_status(self):
        return self.status


class pageNavigationButton(QtWidgets.QPushButton):
    NORMAL_STYLE = """QPushButton{
	border: 0px solid gray;
	font-size: 14px;
	color: rgb(50, 50, 50);
	min-width: 30;
	max-width: 30;
	min-height:30;
	max-height: 30;
    }

    QPushButton:disabled
    {
	color: rgba(120, 120, 120, 255);
    }

    #QPushButton:hover
    {
	font-weight: bold;
	background-color: rgba(247, 248, 250, 100);
	border-radius: 8px;
    }

    """

    SELECT_STYLE = """QPushButton{
    font-weight: bold;
	background-color: rgba(247, 248, 250, 100);
	border-radius: 8px;
    }
    """

    def __init__(self, number, *a, **kw):
        super(pageNavigationButton, self).__init__(*a, **kw)
        self.number = number
        GUIBackend.set_button_text(self, str(self.number))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.set_selected(False)
    
    def set_selected(self, selected):
        if selected:
            GUIBackend.set_style(self, self.NORMAL_STYLE + self.SELECT_STYLE)
        else:
            GUIBackend.set_style(self, self.NORMAL_STYLE)

class viewEyeButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(viewEyeButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(IconsPath.IconsPath.VIEW_EYE_ICON)
        self._icon_over = QtGui.QIcon(IconsPath.IconsPath.VIEW_EYE_ICON_HOVER)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setIcon(self._icon_normal)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(editButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(editButton, self).enterEvent(event)


class viewButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(viewButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(IconsPath.IconsPath.VIEW_ICON)
        self._icon_over = QtGui.QIcon(IconsPath.IconsPath.VIEW_ICON_HOVER)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setIcon(self._icon_normal)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(editButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(editButton, self).enterEvent(event)


class editButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(editButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(IconsPath.IconsPath.EDIT_ICON)
        self._icon_over = QtGui.QIcon(IconsPath.IconsPath.EDIT_ICON_HOVER)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setIcon(self._icon_normal)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(editButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(editButton, self).enterEvent(event)


class deleteButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(deleteButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(IconsPath.IconsPath.DELETE_ICON)
        self._icon_over = QtGui.QIcon(IconsPath.IconsPath.DELETE_ICON_HOVER)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setIcon(self._icon_normal)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(deleteButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(deleteButton, self).enterEvent(event)


class closeButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(closeButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(IconsPath.IconsPath.CLOSE_MESSAGE_ICON)
        self._icon_over = QtGui.QIcon(IconsPath.IconsPath.CLOSE_MESSAGE_ICON)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIcon(self._icon_normal)
        self.setIconSize(QtCore.QSize(14, 14))
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(deleteButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(deleteButton, self).enterEvent(event)


class iconButton(QtWidgets.QPushButton):

    def __init__(self, icon_normal_path, *a, **kw):
        super(iconButton, self).__init__(*a, **kw)
        self._icon_normal = QtGui.QIcon(icon_normal_path)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIcon(self._icon_normal)
        self.setIconSize(QtCore.QSize(24, 24))

    def set_icon(self, icon_normal_path):
        self._icon_normal = QtGui.QIcon(icon_normal_path)
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIcon(self._icon_normal)
        self.setIconSize(QtCore.QSize(24, 24))

class reportButton(QtWidgets.QPushButton):

    def __init__(self, *a, **kw):
        super(reportButton, self).__init__(*a, **kw)
        self._icon = QtGui.QIcon(':/assets/icons/icons8-eye-white-50.png')
        self.setText("")
        self.setStyleSheet(REPORT_BUTTON_STYLE)
        self.setIcon(self._icon)


class tableButton(QtWidgets.QPushButton):

    def __init__(self, text='', *a, **kw):
        super(tableButton, self).__init__(*a, **kw)
        self.setStyleSheet(TABLE_BUTTON_STYLE)
        self.setText(text)

class grabbingStatusButton(QtWidgets.QPushButton):
    def __init__(self, parent: None):
        super(grabbingStatusButton, self).__init__(parent)

    def set_grabbing(self):
        grabbing_icon = IconsPath.IconsPath.GRABBING_ICON
        GUIBackend.set_button_icon(self, grabbing_icon, size=(28, 28))

    def set_not_grabbing(self):
        not_grabbing_icon = IconsPath.IconsPath.NOT_GRABBING_ICON
        GUIBackend.set_button_icon(self, not_grabbing_icon, size=(28, 28))


class tabelCheckbox(QtWidgets.QCheckBox):

    def __init__(self, *a, **kw):
        super(tabelCheckbox, self).__init__(*a, **kw)
        

    # def set_size(self, w, h):
    #     self.setStyleSheet(f"""QCheckBox::indicator 
    #                             {{
    #                            width :{w}px;
    #                            height :{h}px;
    #                            }}""")

    #     #self.setMaximumWidth(h+5)
    #     #self.setMaximumWidth(w+5)


class compareComboBox(QtWidgets.QComboBox):

    def __init__(self, *a, **kw):
        super(compareComboBox, self).__init__(*a, **kw)

        self.insertItems(0, ['none', '>','>=', '<', '<=', '=='])
        self.setStyleSheet(COMPARE_COMBOBOXE)


class Input(QtWidgets.QLineEdit):

    def __init__(self, *a, **kw):
        super(Input, self).__init__(*a, **kw)

        

    def set_size(self, w, h):
        self.setStyleSheet(f"""QLineEdit 
                                {{
                               width :{w}px;
                               height :{h}px;

                               min-width :{w}px;
                               min-height :{h}px;

                               max-width :{w}px;
                               max-height :{h}px;
                               }}""")


class doubleSpinBoxTable(QtWidgets.QDoubleSpinBox):

    def __init__(self, *a, **kw):
        super(doubleSpinBoxTable, self).__init__(*a, **kw)
        self.setStyleSheet(TABLE_SPINBOX)


class LabelTable(QtWidgets.QLabel):
    clicked = QtCore.Signal()
    def __init__(self, *a, **kw):
        super(LabelTable, self).__init__(*a, **kw)
        self.setScaledContents(True)

    def mousePressEvent(self, event:QtCore.QEvent):        
        if event.type() == QtCore.QEvent.MouseButtonPress:
                self.clicked.emit()
  

    
    def set_size(self, h,w):
        GUIBackend.set_max_size(self, h, w)
        GUIBackend.set_min_size(self, h, w)


class inputTable(QtWidgets.QLineEdit):
    def __init__(self, *a, **kw):
        super(inputTable, self).__init__(*a, **kw)


class MessageBox:
    def __init__(self, title, text, buttons, icon_type, parent=None):

        self.STANDARD_BUTTONS = {
            'yes': QtWidgets.QMessageBox.Yes,
            'no': QtWidgets.QMessageBox.No,
            'cancel': QtWidgets.QMessageBox.Cancel,
            'save': QtWidgets.QMessageBox.Save,
            'ok': QtWidgets.QMessageBox.Ok,
            'ignore': QtWidgets.QMessageBox.Ignore,
        }

        self.STANDARD_BUTTONS_STYLES = {
            'yes': YES_BUTTUN_STYLE,
            'no': NO_BUTTUN_STYLE,
            'cancel': CANCEL_BUTTUN_STYLE,
            'save': SAVE_BUTTUN_STYLE,
            'ignore': IGNORE_BUTTUN_STYLE,
            'ok': OK_BUTTUN_STYLE
        }

        self.buttons = buttons

        self.msg = QtWidgets.QMessageBox(parent=parent)
        self.msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.msg.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.msg.setStyleSheet(CONFIRMBOX_STYLESHEET)
        self.msg.setMinimumSize(400, 200)

        if icon_type=='question':
            icon_path = IconsPath.IconsPath.QUESTION_ICON
        if icon_type=='info':
            icon_path = IconsPath.IconsPath.INFO_PATH
        if icon_type=='success':
            icon_path = IconsPath.IconsPath.SUCCESS_ICON
        if icon_type=='warning':
            icon_path = IconsPath.IconsPath.WARNING_ICON
        if icon_type=='error':
            icon_path = IconsPath.IconsPath.ERROR_ICON

        self.icon = QtGui.QPixmap(icon_path)
        self.msg.setIconPixmap(self.icon)

        # self.msg.setText("{0} <br> {0}".format(title, text))

        html_text = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        /* Title style */
        .title {{
            color: rgb(20, 20, 20); /* Title color */
            font-size: 22px; /* Title font size */
            font-weight: bold;
        }}
        /* Text style */
        .text {{
            color: rgb(20, 20, 20);
            font-size: 16px; /* Text font size */
        }}
        </style>
        </head>
        <body>
        <p class="title">{0}</p>
        <p class="text">{1}</p>
        </body>
        </html>
        """
        self.msg.setTextFormat(QtCore.Qt.RichText)
        self.msg.setText(html_text.format(title, text))

        #---------------------------------------------------
        selected_buttons_obj = []
        for btn_name in buttons:
            btn = self.STANDARD_BUTTONS[btn_name]
            if isinstance(selected_buttons_obj, list):
                selected_buttons_obj = btn
            else:
                selected_buttons_obj = selected_buttons_obj | btn
        self.msg.setStandardButtons(selected_buttons_obj)
        #---------------------------------------------------

        for btn_name in buttons:
            style = self.STANDARD_BUTTONS_STYLES[btn_name]
            btn = self.msg.button(self.STANDARD_BUTTONS[btn_name])
            btn.setStyleSheet(style)

    def render(self) -> str:
        retval = self.msg.exec_()
        for btn_name in self.buttons:
            if self.STANDARD_BUTTONS[btn_name] == retval:
                return btn_name


class timerBuilder:

    def __init__(self, t, event_func) -> None:
        self.event_func = event_func
        self.t = t
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect( self.event_func)


    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.event_func)
        self.timer.start(self.t)
    

    def stop(self, ):
        self.timer.stop()
        self.timer.deleteLater()


class singleAnimation:
    EASING_CURVES = {
        'linear': QtCore.QEasingCurve.Linear,
        'in_out_fast': QtCore.QEasingCurve.InOutExpo,
        'in_out_slow': QtCore.QEasingCurve.InOutCirc,
    }

    def __init__(self, obj ,atribute, time, key1, key2, easing_curve='linear') -> None:
        
        self.key1 = key1
        self.key2 = key2
        self.time = time
        self.toggle_flag = True
        self.animation = QtCore.QPropertyAnimation(obj, atribute)
        self.animation.setDuration(time)
        self.animation.setEasingCurve(self.EASING_CURVES[easing_curve])
    
    def reset(self,):
        self.animation.setDuration(1)
        self.animation.setStartValue(self.key1)
        self.animation.setEndValue(self.key1)
        self.animation.start()
        self.animation.setDuration(self.time)
        
    
    def forward( self ):
        self.toggle_flag = False
        self.animation.setStartValue(self.key1)
        self.animation.setEndValue(self.key2)
        self.animation.start()
        
    
    def backward(self):
        self.toggle_flag = True
        self.animation.setStartValue(self.key2)
        self.animation.setEndValue(self.key1)
        self.animation.start()
        


    def single_forward(self):
        if self.toggle_flag:
            self.forward()
            
        
    
    def single_backward(self,):
        if not self.toggle_flag:
            self.backward()
    
    
    def toggle(self,):
        if self.toggle_flag:
            self.forward()
        else:
            self.backward()


class gifPlayer:

    def __init__(self, label: QtWidgets.QLabel, gif_path: str) -> None:
        self.movie = QtGui.QMovie(gif_path)
        self.label = label
        self.label.setMovie(self.movie)

        self.max_w = self.label.maximumWidth()
        self.max_h = self.label.maximumHeight()
    
    def set_maxsize(self, max_h, max_w):
        if max_w is not None:
            self.max_w = max_w
        
        if max_h is not None:
            self.max_h = max_h


	# Start Animation
    def start_animation(self):
        self.movie.start()

    def show_and_start_animation(self,):
        self.label.setMaximumHeight(self.max_h)
        self.label.setMaximumWidth(self.max_w)

        self.start_animation()

	# Stop Animation(According to need)
    def stop_animation(self):
        pass
        #self.movie.startTimer()

    def hide_and_stop_animation(self,):
        self.label.setMaximumHeight(0)
        self.label.setMaximumWidth(0)

        self.stop_animation()


def selectDirectoryDialog():
    path = QtWidgets.QFileDialog.getExistingDirectory()
    return path


def selectSaveFile(file_name:str = 'All', file_extention:str='.*'):
    """opens a dialog file to select a file to save

    Args:
        file_name (str): an ideal name of file like 'Excel' 
        file_extention (str): file extention like '.xlsx'

    Returns:
        _type_: selected path
    """
    filter = f'{file_name} (*{file_extention})'
    path = QtWidgets.QFileDialog.getSaveFileName(filter=filter)
    return path


def selectFileDialog(file_name:str = 'All', file_extention:str='.*'):
    """opens a dialog file to select a file to save

    Args:
        file_name (str): an ideal name of file like 'Excel' 
        file_extention (str): file extention like '.xlsx'

    Returns:
        _type_: selected path
    """
    filter = f'{file_name} (*{file_extention})'
    path = QtWidgets.QFileDialog.getOpenFileName(filter=filter)
    return path


class overlayMassage(QtWidgets.QWidget):
    def __init__(self, 
                 text,
                 fill_overlay_color:tuple=(30, 30, 30, 200),
                 popup_bg:tuple=(0,0,0,0),
                 popup_card_size = (120,300),
                 font_size = 48,
                 text_color:tuple = (220,220,220), 
                 parent=None):
        
        super(overlayMassage, self).__init__()

        self.text = text
        self.popup_bg = QtGui.QColor(*popup_bg)
        self.overlay_color = fill_overlay_color
        self.fill_overlay_color = QtGui.QColor(*fill_overlay_color)
        self.popup_fillColor = QtGui.QColor(*popup_bg)
        self.popup_card_size = popup_card_size
        self.font_size = font_size
        self.text_color = text_color

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)




    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setBrush(self.fill_overlay_color)
        qp.drawRect(0, 0, s.width(), s.height())

        # drawpopup
        qp.setBrush(self.popup_bg)
        qp.setPen(self.popup_bg)
        popup_width = self.popup_card_size[0]
        popup_height = self.popup_card_size[1]
        ow = int(s.width()/2-popup_width/2)
        oh = int(s.height()/2-popup_height/2)
        qp.drawRoundedRect(ow, oh, popup_width, popup_height, 5, 5)

        font = QtGui.QFont()
        font.setPixelSize(self.font_size)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QtGui.QColor(*self.text_color))
        tolw, tolh = 80, -5
        qp.drawText(ow + int(popup_width/2) - tolw, oh + int(popup_height/2) - tolh, self.text)

        qp.end()


    def show(self,):
        self.showMaximized()

class defectNotification(QtWidgets.QWidget):

    def __init__(self, 
                 id: int,
                 side:str,
                 tag:str,
                 datetime:datetime,  
                 defect_type:str ,
                 defect_color:tuple) -> None:
        
        super(defectNotification, self).__init__()
        self.ui = Ui_Notification()
        self.ui.setupUi(self)

        self.side = side
        self.tag = tag
        self.datetime = datetime
        self.defect_type = defect_type
        self.defect_color = defect_color
        self.id = id
        self.__is_seen = False

        self.set_side(self.side)
        self.set_tag(self.tag)
        self.set_date(self.datetime.date())
        self.set_time(self.datetime.time())
        self.set_defect_color(self.defect_color)
        self.set_defect_type(self.defect_type)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.external_select_event_func(self)

    def select_connector(self, func):
        self.external_select_event_func = func

    def close_connector(self, func):
        GUIBackend.button_connector_argument_pass(self.ui.close_btn,
                                                  func,
                                                  (self,) )

    def set_side(self, side:str):
        self.ui.side_label.setText(side.capitalize())
    
    def set_tag(self, tag:str):
        self.tag = tag
        if tag:
            if self.__is_seen:
                tag = f'({tag})'
            else:
                tag = f'({tag}*)'

        self.ui.tag_label.setText(tag.capitalize())

    def set_seen(self, flag):
        self.__is_seen = flag
        self.set_tag(self.tag)
    
    def set_defect_type(self, defect_type:str):
        self.ui.defect_type_label.setText(defect_type)

    def set_date(self, date:date):
        today = date.today()
        diff = today - date
        if diff.days > 10 :
            txt = date.strftime("%Y/%m/%d")
        elif diff.days == 0:
            txt = 'today'
        else:
            txt = f'{diff.days} days ago'
        self.ui.date_label.setText(txt)
    
    def set_time(self, t:datetime.time):
        txt = t.strftime('%H:%M:%S')
        self.ui.time_label.setText(txt)

    def set_defect_color(self, color:tuple):
        style = f"""
            #defect_color_frame{{
            background-color: rgb{color};
            border-radius:15px;
            border: None;
        }}
        """
        self.ui.defect_color_frame.setStyleSheet(style)
    
    def is_checked(self,):
        return self.ui.select_checkBox.isChecked()
    
    
    def set_selected(self,flag):
        style = """
            #main_frame{{
            background-color: rgb{0};
            border:1px solid #E0E4EC;
            border-radius: 15px;
        }}
        """
        if flag:
            self.ui.main_frame.setStyleSheet(style.format("(194, 204, 238)"))
        else:
            self.ui.main_frame.setStyleSheet(style.format("(247, 248, 250)"))

    def set_checkbox(self, flag):
        self.ui.select_checkBox.setChecked(flag)


class proggressDialogUI(QtWidgets.QWidget):

    def __init__(self, title='',
                       description='',
                       show_info = True,
                       operation_name='') -> None:

        super(proggressDialogUI, self).__init__()
        self.ui = Ui_progressDialog()
        self.ui.setupUi(self)

        self.progressbar = self.ui.progressbar
        self.title_lbl = self.ui.title_lbl
        self.description_lbl = self.ui.description_lbl
        self.progress_operetion_lbl = self.ui.progress_operetion_lbl
        self.value_lbl = self.ui.progressbar_value_label
        self.progress_frame = self.ui.progress_frame
        self.complete_count_lbl = self.ui.complete_count_lbl
        self.total_count_lbl = self.ui.total_count_lbl
        self.cancel_btn = self.ui.cancel_btn

        self.setup(title, description, show_info, operation_name)
        GUIBackend.set_win_frameless(self)
        GUIBackend.set_win_attribute(self, QtCore.Qt.WA_TranslucentBackground)

        self.move_refresh_time = 0
        self.offset = None

        self._center()

    def _center(self):
        # Get primary screen
        primary_screen = QApplication.primaryScreen()

        if primary_screen:
            # Get geometry of the primary screen
            screen_geometry = primary_screen.geometry()

            # Calculate center point
            center_point = screen_geometry.center()

            # Set window position to be centered
            self.move(center_point.x() - self.frameGeometry().width() // 2,
                      center_point.y() - self.frameGeometry().height() // 2)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = QtCore.QPoint(event.position().x(),event.position().y())
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            if time.time() - self.move_refresh_time > Constant.RefreshRates.MOUSE_MOVE:
                self.move_refresh_time = time.time()
                self.move(self.pos() + QtCore.QPoint(event.scenePosition().x(),event.scenePosition().y()) - self.offset)

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def setup(self, title='',
                       description='',
                       show_info = True,
                       operation_name=''):
        
        
        
        GUIBackend.set_wgt_visible(self.progress_frame, show_info)
        GUIBackend.set_label_text(self.title_lbl, title)
        GUIBackend.set_label_text(self.description_lbl, description)
        GUIBackend.set_label_text(self.title_lbl, title)
        GUIBackend.set_label_text(self.progress_operetion_lbl, operation_name)

    
    

    def set_delete_progress_value(self, n, total=100):
        GUIBackend.set_label_text(self.complete_count_lbl, str(int(n)))
        GUIBackend.set_label_text(self.total_count_lbl, str(total))

        percent = n / total * 100
        GUIBackend.set_label_text(self.value_lbl, str(round(percent)))
        GUIBackend.set_progressbar_value(self.progressbar, percent)

    def cancel_button_connector(self,func):
        GUIBackend.button_connector(self.cancel_btn, func)

    
    def show_confirm_massage(self, title, text, buttons, icon_type):
        dialog =  MessageBox(title, text, buttons, icon_type, parent=self)
        return dialog.render()


    def show_win(self,):
        GUIBackend.show_window(self, always_on_top=True)
    
    def close_win(self):
        GUIBackend.close_window(self)

    def hide_win(self,):
        GUIBackend.hide_window(self)






class MplCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

        self.default_xlim = (0, 1)
        self.default_ylim = (0, 1)

        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.press_event = None

    def setup_design(self):
        # Adjust layout padding
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.figure.tight_layout(pad=0.2)

    def plot_data(self, *trends, scale=False, bg_color='white'):
        self.figure.patch.set_facecolor(bg_color)
        self.axes.set_facecolor(bg_color)

        # Store axis limits before clearing the plot
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        self.axes.clear()
        for tr in trends:
            xs, ys, color = tr
            self.axes.plot(xs, ys, color=color)

        if scale:
            self.axes.set_aspect('equal')

        # Reapply axis limits
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

        self.setup_design()
        self.canvas.draw()

    def set_axis_ranges(self, x_range=None, y_range=None):
        if x_range:
            self.axes.set_xlim(x_range)
            self.default_xlim = x_range
        if y_range:
            self.axes.set_ylim(y_range)
            self.default_ylim = y_range
        self.canvas.draw()

    def on_scroll(self, event):
        """Handle zooming in and out with the mouse scroll."""
        base_scale = 1.1
        if event.step > 0:
            scale_factor = 1 / base_scale
        else:
            scale_factor = base_scale
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        xdata, ydata = event.xdata, event.ydata

        if xdata is not None and ydata is not None:
            new_xlim = [
                xdata - (xdata - xlim[0]) * scale_factor,
                xdata + (xlim[1] - xdata) * scale_factor
            ]
            new_ylim = [
                ydata - (ydata - ylim[0]) * scale_factor,
                ydata + (ylim[1] - ydata) * scale_factor
            ]
            self.axes.set_xlim(new_xlim)
            self.axes.set_ylim(new_ylim)
            self.canvas.draw()

    def on_press(self, event):
        if event.button == 1 and event.xdata is not None and event.ydata is not None:
            self.press_event = event

    def on_release(self, event):
        if event.button == 1:
            self.press_event = None

    def on_motion(self, event):
        if self.press_event is None or event.button != 1:
            return
        if event.xdata is None or event.ydata is None:
            return
        dx = event.xdata - self.press_event.xdata
        dy = event.ydata - self.press_event.ydata
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        new_xlim = [xlim[0] - dx, xlim[1] - dx]
        new_ylim = [ylim[0] - dy, ylim[1] - dy]
        self.axes.set_xlim(new_xlim)
        self.axes.set_ylim(new_ylim)
        self.canvas.draw()
        self.press_event = event

class DashedLineFrame(QtWidgets.QFrame):
    """
    A QFrame subclass that draws only a vertical dashed line with a width that fits the line.
    """
    def __init__(self, parent=None, line_width=2, line_color="black"):
        super().__init__(parent)
        self.line_width = line_width  # Thickness of the dashed line
        self.line_color = QtGui.QColor(line_color)  # Convert string to QColor
        self.setFixedWidth(self.line_width + 4)  # Adjust frame width to fit the line
        self.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(self.line_color, self.line_width, QtGui.Qt.DashLine)  # Dashed line pen
        painter.setPen(pen)

        # Draw vertical dashed line in the center of the frame
        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())  # Vertical line from top to bottom
        painter.end()