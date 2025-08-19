import sys
import os
import traceback
sys.path.append(os.path.join('UIFiles', 'assets'))
sys.path.append('uiUtils')

#os.system('pyside6-rcc {} -o {}'.format(os.path.join('UIFiles', 'assets', 'assets.qrc'), os.path.join('UIFiles', 'assets', 'assets_rc.py')))
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