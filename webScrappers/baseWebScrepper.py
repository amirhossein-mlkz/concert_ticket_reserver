from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from abc import ABC, abstractmethod

class baseWebScrepper(ABC):

    def __init__(self,):
        
        self.sans_btns = []
        self.chairs = []
        self.current_sans_idx = 0
        self.build()

    def build(self,):
        self.driver = webdriver.Chrome()

    def go_to_url(self, url):
        self.driver.get(url)
        #self.driver.maximize_window()


    @abstractmethod
    def find_sans_buttons(self):
        """Return list of reserve button elements."""
        return self.sans_btns 
    
    @abstractmethod
    def auto_reserve(self,):
        pass


    def close(self):
        self.driver.quit()

    