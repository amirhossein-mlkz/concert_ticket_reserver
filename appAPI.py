from appUI import appUI
from webScrappers.melotikWebScreapper import melotikWebScrepper
from webScrappers.honarticketWebScreapper import honarticketWebScreapper
from webScrappers.baseWebScrepper import baseWebScrepper

from webScrappers.StatusCodes import StatusCodes
from infoSaver import infoSaver
from backend.myLogger import myLogger, LOG_SEPRATOR

class appAPI:

    def __init__(self, uiHandler:appUI):
        self.uiHandler = uiHandler
        self.webScrappers:dict[str, melotikWebScrepper] = { 'melotik':melotikWebScrepper(),
                                                            'honarticket': honarticketWebScreapper(),
                                                        }
        self.infoSaver = infoSaver('user.json')
        self.logger = myLogger().get_logger()



        self.uiHandler.reserve_btn_connector(self.start_reserve)
        self.uiHandler.save_info_button_connector(self.save_info)
        self.load_info()
        self.uiHandler.show_error('')

        

        self.logger.info("software init")
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
        args = {}
        args['honarticket_refresh'] = self.uiHandler.get_honarticket_refresh()
        
        self.logger.info(LOG_SEPRATOR)
        self.logger.info("Start reserve on Settings")
        self.logger.info(f"url: {url}")
        self.logger.info(f"user_info: {user_info}")
        self.logger.info(f"ticket_count: {ticket_count}")
        self.logger.info(f"sans_idx: {sans_idx}")
        self.logger.info(f"chairs range: {start_chair} - {end_chair}")
        self.logger.info(f"args: {args}")
        self.logger.info(LOG_SEPRATOR)







        select_webScrapper = None
        for key, webScrapper in self.webScrappers.items():
            if key in url:
                self.logger.info(f"detected webscrapper: {key}")
                select_webScrapper = webScrapper

        if select_webScrapper is None:
            self.logger.warning(f"no webscrapper founded for '{url}'")
            self.uiHandler.show_error('سایت مورد نظر تعریف نشده است')
            return
        

        status = select_webScrapper.auto_reserve(url,
                                                 sans_idx, 
                                                 user_info, 
                                                 ticket_count, 
                                                 min_price,
                                                 start_chair=start_chair,
                                                 end_chair=end_chair,
                                                 args = args)
        if status == StatusCodes.NO_SANS_FOUND:
            self.uiHandler.show_error(' خطا، سانس مورد نظر یافت نشد')
            return
        
        if status == StatusCodes.NO_CHAIR_FOUND:
            self.uiHandler.show_error(' خطا،  صندلی برای رزرو یافت نشد')
        

    
