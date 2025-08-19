from UIFiles.main_UI import Ui_MainWindow
from PySide6 import QtWidgets
from PySide6 import QtGui

from GUIComponents import SwitchControl

class Styler:

    def __init__(self, ui:Ui_MainWindow) -> None:
        self.ui = ui

        self.shadows_obj: dict[QtWidgets.QWidget] = {
            'save':
                {   
                    'style': {'blur_radius':15,
                              'offset':(3,3),
                              'color':(0,0,0,100),
                              },
                    'objects':[ #self.ui.save_camera_settings,
                                # self.ui.cancel_camera_settings,
                                # self.ui.save_algorithm_settings,
                                # self.ui.cancel_algorithm_settings,
                                # self.ui.register_user,
                                # self.ui.userpage_editprofile_change_username_btn,
                                # self.ui.userpage_editprofile_change_password_btn,
                                # self.ui.report_filter_apply_btn,
                                ]
                },

            'frame':
                {   
                    'style': {'blur_radius':10,
                              'offset':(1,1),
                              'color':(0,0,0,50),
                              },
                    'objects':[ self.ui.step1_settings_frame,
                                self.ui.step2_settings_frame,
                                self.ui.step3_settings_frame,

                                # self.ui.camera_settings_frame,
                                ]
                },


            # 'groupbox':
            #     {   
            #         'style': {'blur_radius':20,
            #                   'offset':(5,5),
            #                   'color':(0,0,0,50),
            #                   },
            #         'objects':[ self.ui.userpage_editprofile_edit_profile_groupbox,
            #                     self.ui.userpage_editprofile_change_pass_groupbox,
            #                     ]
            #     },

        }

        self.layout_obj: dict[QtWidgets.QWidget] = {
            'message': 
                {   
                    'style': {'layout_type': 'vertical',
                              'spacer_type': 'vertical'
                              },
                    'objects':[ self.ui.register_message_frame,
                                self.ui.change_username_message_frame,
                                self.ui.change_password_message_frame
                                ]
                },
        } 

        self.spliter_obj = {
            self.ui.camera_settings_splitter: [358, 550],
            self.ui.belt_view_splitter: [362, 574]
        }

        self.switch_objs: dict[SwitchControl, int] = {
            self.ui.connect_camera_switch: 2,
            self.ui.algo_connect_camera_switch: 1,
        }

    def render(self,):
        self.__set_shadow()
        self.__set_layout()
        self.set_spliter_init_size()
        self.set_switches_size()

    def __set_shadow(self, ):
        for group_name, group in self.shadows_obj.items():
            style = group['style']
            objects:list[QtWidgets.QWidget] = group['objects']
            for obj in objects:
                shadow  = QtWidgets.QGraphicsDropShadowEffect(obj)
                shadow.setBlurRadius(style['blur_radius'])
                shadow.setOffset(*style['offset'])
                shadow.setColor(QtGui.QColor(*style['color']))
                obj.setGraphicsEffect(shadow)

    def __set_layout(self, ):
        for group_name, group in self.layout_obj.items():
            style = group['style']
            objects:list[QtWidgets.QWidget] = group['objects']
            for obj in objects:
                layout = QtWidgets.QHBoxLayout() if style['layout_type']=='horizontal' else QtWidgets.QVBoxLayout()
                spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum) if style['layout_type']=='horizontal' \
                    else QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
                obj.setLayout(layout)
                layout.addItem(spacer)

    def set_spliter_init_size(self):
        obj: QtWidgets.QSplitter
        for obj, sizes in self.spliter_obj.items():
            obj.setSizes(sizes)

    def set_switches_size(self):
        for switch, size in self.switch_objs.items():
            switch.change_size(size)
