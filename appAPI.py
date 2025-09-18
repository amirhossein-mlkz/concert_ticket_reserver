from appUI import appUI
from webScrappers.melotikWebScreapper import melotikWebScrepper
from webScrappers.honarticketWebScreapper import honarticketWebScreapper
from webScrappers.baseWebScrepper import baseWebScrepper

from webScrappers.StatusCodes import StatusCodes
from infoSaver import infoSaver

class appAPI:

    def __init__(self, uiHandler:appUI):
        self.uiHandler = uiHandler
        self.webScrappers:dict[str, melotikWebScrepper] = { 'melotik.com':melotikWebScrepper(),
                                                            'honarticket.com': honarticketWebScreapper(),
                                                        }
        self.infoSaver = infoSaver('user.json')

        self.uiHandler.ui.input_url.setText('https://www.honarticket.com/nushe12')


        self.uiHandler.reserve_btn_connector(self.start_reserve)
        self.uiHandler.save_info_button_connector(self.save_info)
        self.load_info()
        self.uiHandler.show_error('')

        


        self.uiHandler.show()

    def save_info(self,):
        info  = self.uiHandler.get_reserver_info()
        self.infoSaver.save(info)
    
    def load_info(self,):
        info = self.infoSaver.load()
        self.uiHandler.set_reserver_info(info)
    
    def start_reserve(self, ):
        self.uiHandler.show_error('')
        url = self.uiHandler.get_input_link()
        user_info = self.uiHandler.get_reserver_info()
        ticket_count = self.uiHandler.get_reserve_count()
        min_price = self.uiHandler.get_min_price()
        sans_idx = self.uiHandler.get_sans_idx()
        start_chair , end_chair = self.uiHandler.get_chair_range()

        select_webScrapper = None
        for key, webScrapper in self.webScrappers.items():
            if key in url:
                select_webScrapper = webScrapper

        if select_webScrapper is None:
            self.uiHandler.show_error('سایت مورد نظر تعریف نشده است')
            return
        

        status = select_webScrapper.auto_reserve(url,
                                                 sans_idx, 
                                                 user_info, 
                                                 ticket_count, 
                                                 min_price,
                                                 start_chair=start_chair,
                                                 end_chair=end_chair)
        if status == StatusCodes.NO_SANS_FOUND:
            self.uiHandler.show_error(' خطا، سانس مورد نظر یافت نشد')
            return
        
        if status == StatusCodes.NO_CHAIR_FOUND:
            self.uiHandler.show_error(' خطا،  صندلی برای رزرو یافت نشد')
        

    
