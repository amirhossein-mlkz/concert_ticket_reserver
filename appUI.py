from PySide6.QtWidgets import QMainWindow, QHeaderView, QApplication
from PySide6 import QtCore
from UIFiles.main_UI import Ui_MainWindow

from uiUtils.guiBackend import GUIBackend

class appUI(QMainWindow):

    """this class is used to build class for mainwindow to load GUI application

    :param QtWidgets: _description_

    """
    def __init__(self):
        """this function is used to laod ui file and build GUI application"""
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_info = {'phone':self.ui.phone_input,
                          'name':self.ui.name_input,
                          'family': self.ui.family_input,
                          }


    def get_input_link(self,) -> str:
        return GUIBackend.get_input(self.ui.input_url)
    
    def reserve_btn_connector(self, func):
        GUIBackend.button_connector(self.ui.start_reserve_btn, func)

    def show_error(self,txt):
        GUIBackend.set_label_text(self.ui.log_label, txt)

    def save_info_button_connector(self, func):
        GUIBackend.button_connector(self.ui.save_info, func)


    def get_reserver_info(self,) -> dict:
        res = {}
        for key , field in self.user_info.items():
            res[key] = GUIBackend.get_input(field)
        return res
    
    def get_reserve_count(self,):
        return GUIBackend.get_input(self.ui.reserve_count)
    
    def get_min_price(self,):
        return GUIBackend.get_input(self.ui.min_price)
    
    def get_sans_idx(self,):
        return GUIBackend.get_input(self.ui.sans_idx)
    
    def set_reserver_info(self, info:dict):
        for key , value in info.items():
            GUIBackend.set_input(self.user_info[key], value)

    def get_chair_range(self,):
        start = -1
        end = -1
        if GUIBackend.get_checkbox_value(self.ui.start_chair_checkbox):
            start = GUIBackend.get_input(self.ui.start_chair)
        
        if GUIBackend.get_checkbox_value(self.ui.end_chair_checkbox):
            end = GUIBackend.get_input(self.ui.end_chair)
        
        return start , end
    
    def get_honarticket_refresh(self,):
        return  GUIBackend.get_checkbox_value(self.ui.refresh_honar_ticket_checkbox)