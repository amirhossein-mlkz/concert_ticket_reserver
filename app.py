import sys
import os
import traceback
sys.path.append('UIFiles')
# sys.path.append('uiUtils')

BUILD = False
if BUILD:
    os.system('pyside6-rcc {} -o {}'.format(os.path.join('UIFiles', 'resource.qrc'), os.path.join('UIFiles', 'resource_rc.py')))
    os.system('pyside6-uic {} -o {}'.format(os.path.join('UIFiles', 'main_UI.ui'), os.path.join('UIFiles', 'main_UI.py')))



from PySide6.QtWidgets import QApplication
from appAPI import appAPI
from appUI import appUI
# from main_UI import mainUI



if __name__ == "__main__":
    app = QApplication(sys.argv)

    
    
    main_ui = appUI()
    API = appAPI(main_ui)
    #main_ui.show()
    app.exec()