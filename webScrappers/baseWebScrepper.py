from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException,WebDriverException
import os
import time
from abc import ABC, abstractmethod
from .StatusCodes import StatusCodes

class baseWebScrepper(ABC):

    def __init__(self,):
        
        self.sans_btns = []
        self.chairs:dict = {}
        self.current_sans_idx = 0
        # self.build()

    def build(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'  # فقط تا DOM اولیه لود شود

        # خاموش کردن GCM و PushMessaging
        options.add_argument("--disable-features=GCM,PushMessaging")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-default-apps")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")

        # بلاک کردن نوتیفیکیشن‌ها
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        # حذف لاگ‌های اضافه
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # فرستادن لاگ chromedriver به /dev/null (یا nul در ویندوز)
        service = Service(log_path=os.devnull)

        self.driver = webdriver.Chrome(service=service, options=options)

    def go_to_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()


    @abstractmethod
    def find_sans_buttons(self):
        """Return list of reserve button elements."""
        return self.sans_btns 
    
    @abstractmethod
    def auto_reserve(self,):
        pass


    def close(self):
        self.driver.quit()


    def scroll_into_view_if_needed(self, element, sleep_time=0.3):
        # گرفتن مختصات قبل از اسکرول
        before = element.location_once_scrolled_into_view

        # اسکرول به المنت
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        # گرفتن مختصات بعد از اسکرول
        after = element.location_once_scrolled_into_view

        # اگر مختصات تغییر کرده بود → اسکرول واقعی انجام شده
        if before != after:
            time.sleep(sleep_time)

    def is_in_viewport(self, element, margin_top=200, margin_bottom=200):
        """
        چک می‌کند المان حداقل بخشی داخل ویوپورت باشد و از بالا و پایین صفحه مارجین مشخصی رعایت شود.
        
        :param element: WebElement
        :param margin_top: فاصله از بالای صفحه (پیکسل)
        :param margin_bottom: فاصله از پایین صفحه (پیکسل)
        :return: True/False
        """
        return self.driver.execute_script("""
            var elem = arguments[0];
            var marginTop = arguments[1];
            var marginBottom = arguments[2];

            var rect = elem.getBoundingClientRect();
            var viewHeight = (window.innerHeight || document.documentElement.clientHeight);

            // بررسی اینکه بخشی از المان داخل ویوپورت باشه
            var visible = rect.bottom > marginTop && rect.top < (viewHeight - marginBottom);

            return visible;
        """, element, margin_top, margin_bottom)

    def safe_click(self, element, scroll=True, use_js=True):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
            
            if scroll and not self.is_in_viewport(element):
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.1)

            element.click()
            return True
        except ElementClickInterceptedException:
            if use_js:
                print("Element was intercepted, using JavaScript click.")
                self.driver.execute_script("arguments[0].click();", element)
                return True
            return False
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def is_chair_in_range(self, chair_num, start, end):
        if chair_num is None:
            return False
        if start > 0 and chair_num < start:
            return False
        if end > 0 and chair_num > end:
            return False
        return True
    
    def print_chairs(self, chair_items:dict=None ):
        if chair_items is None:
            self.chairs.items()
        for rn, rn_chairs in chair_items:
            for i in range(len(rn_chairs['chairs_num'])):
                num = rn_chairs['chairs_num'][i]
                price = rn_chairs['chairs_price'][i]
                print(f"{rn} : {num} - {price}$")


    def check_single_chair_for_concert(self,idx , chairs_num, chairs_reservable, remain_chair, start_chair=-1, end_chair=-1):
        i = idx
        this_chair_num = chairs_num[i]
        next_chair_num = chairs_num[i+1] if i+1 < len(chairs_num) else None
        next_next_chair_num = chairs_num[i+2] if i+2 < len(chairs_num) else None
        next_next_next_chair_num = chairs_num[i+3] if i+3 < len(chairs_num) else None
        prev_chair_num = chairs_num[i-1] if i>=1 else None
        prev_prev_chair_num = chairs_num[i-2] if i>=2 else None
        prev_prev_prev_chair_num = chairs_num[i-3] if i>=3 else None

        
        next_chair_reservable = chairs_reservable[i+1] if i+1 < len(chairs_num) else False
        next_next_chair_reservable = chairs_reservable[i+2] if i+2 < len(chairs_num) else False
        # next_next_next_chair_reservable = chairs_reservable[i+3] if i+3 < len(chairs_num) else False
        prev_chair_reservable = chairs_reservable[i-1] if i>=1 else None
        prev_prev_chair_reservable = chairs_reservable[i-2] if i>=2 else None

        if next_chair_num is not None and (abs(next_chair_num - this_chair_num) != 1):
            next_chair_num = None
            next_next_chair_num = None
            next_next_next_chair_num = None
        
        if prev_chair_num is not None and (abs(prev_chair_num - this_chair_num) != 1):
            prev_chair_num = None
            prev_prev_chair_num = None
            prev_prev_prev_chair_num = None

        if next_next_chair_num is not None and(abs(next_next_chair_num - this_chair_num)!=2):
            next_next_chair_num = None
            next_next_next_chair_num = None
        
        if prev_prev_chair_num is not None and(abs(prev_prev_chair_num - this_chair_num)!=2):
            prev_prev_chair_num = None
            prev_prev_prev_chair_num = None

        if next_next_next_chair_num is not None and(abs(next_next_next_chair_num - this_chair_num)!=3):
            next_next_next_chair_num = None

        if prev_prev_prev_chair_num is not None and(abs(prev_prev_prev_chair_num - this_chair_num)!=3):
            prev_prev_prev_chair_num = None
        #------------------------------------------------------------------------------------------------
        # if not self.is_chair_in_range(prev_chair_num, start_chair, end_chair):
        #     prev_chair_num = None

        # if not self.is_chair_in_range(prev_prev_chair_num, start_chair, end_chair):
        #     prev_prev_chair_num = None

        # if not self.is_chair_in_range(prev_prev_prev_chair_num, start_chair, end_chair):
        #     prev_prev_prev_chair_num = None

        # if not self.is_chair_in_range(next_chair_num, start_chair, end_chair):
        #     next_chair_num = None

        # if not self.is_chair_in_range(next_next_chair_num, start_chair, end_chair):
        #     next_next_chair_num = None

        # if not self.is_chair_in_range(next_next_next_chair_num, start_chair, end_chair):
        #     next_next_next_chair_num = None
            
        
        if remain_chair<=0: #max_reserve == reserve_count + 1:
            #o*x
            #oox
            if  next_next_chair_num is None and next_chair_num is not None:
                return False
            #o*o
            if (    (next_chair_num is not None and not next_chair_reservable) 
                and (next_next_chair_num is not None and next_next_chair_reservable)):
                return False
            #oo*
            if (    (next_chair_num is not None and next_chair_reservable)
                and (next_next_chair_num is not None and not next_next_chair_reservable)
                ):
                return False

        #: o could reserve
        #: * couldn't resservable
        #: x not exist   
        #: n we don't want reserve
        
        #o*x        ->
        if next_chair_num is not None and not next_chair_reservable and next_next_chair_num is None:
            return False
        #x*o        <-
        if prev_chair_num is not None and not prev_chair_reservable and prev_prev_chair_num is None:
            return False
        #oo*X       ->
        if (    next_chair_num is not None and next_chair_reservable 
            and next_next_chair_num is not None and not next_next_chair_reservable
            and next_next_next_chair_num is None):
            return False
        
        #x*oo       <-
        if (    prev_chair_num is not None and prev_chair_reservable 
            and prev_prev_chair_num is not None and not prev_prev_chair_reservable
            and prev_prev_prev_chair_num is None):
            return False
        
        #xno  <-
        if (    prev_chair_num is not None and not self.is_chair_in_range(prev_chair_num, start_chair, end_chair)
            and prev_prev_chair_num is None):
            return False
        
        #*no  <-
        if (    prev_chair_num is not None and not self.is_chair_in_range(prev_chair_num, start_chair, end_chair)
            and prev_prev_chair_num is not None and not prev_prev_chair_reservable):
            return False
        
        #onx ->
        if (    next_chair_num is not None and not self.is_chair_in_range(next_chair_num, start_chair, end_chair)
            and next_next_chair_num is None):
            return False
        
        #on* ->
        if (    next_chair_num is not None and not self.is_chair_in_range(next_chair_num, start_chair, end_chair)
            and next_next_chair_num is not None and not next_next_chair_reservable):
            return False
        
    
        
        return True
    

    def check_single_chair_for_myself(self, 
                                      idx ,
                                      rn_selected_chairs_num:list,  
                                      chairs_num, 
                                      chairs_reservable, 
                                      remain_chair, 
                                      start_chair=-1, 
                                      end_chair=-1):
        i = idx
        this_chair_num = chairs_num[i]
        next_chair_num = chairs_num[i+1] if i+1 < len(chairs_num) else None
        prev_chair_num = chairs_num[i-1] if i>=1 else None

        can_reserve_next_chair = False
        if idx+1 < len(chairs_num):
            can_reserve_next_chair = self.check_single_chair_for_concert(idx+1, 
                                                                        chairs_num,
                                                                        chairs_reservable,
                                                                        remain_chair-1,
                                                                        start_chair,
                                                                        end_chair)
        
        can_reserve_prev_chair = False
        if idx-1 >= 0:
            can_reserve_prev_chair = self.check_single_chair_for_concert(idx-1, 
                                                                        chairs_num,
                                                                        chairs_reservable,
                                                                        remain_chair-1,
                                                                        start_chair,
                                                                        end_chair)

        #--------------------------------
        if not self.is_chair_in_range(next_chair_num, start_chair, end_chair):
            next_chair_num = None

        if not self.is_chair_in_range(prev_chair_num, start_chair, end_chair):
            prev_chair_num = None

        #--------------------------------
        if next_chair_num is not None and (abs(next_chair_num - this_chair_num) != 1):
            next_chair_num = None

        
        if prev_chair_num is not None and (abs(prev_chair_num - this_chair_num) != 1):
            prev_chair_num = None

        #----------------------------------------------------------------------------

        #XoX
        if next_chair_num is None and prev_chair_num is None:
            return False
        
        if next_chair_num in rn_selected_chairs_num:
            return True
        elif prev_chair_num in rn_selected_chairs_num:
            return True
        

        if next_chair_num is not None and can_reserve_next_chair and remain_chair > 0 :
            return True
        elif prev_chair_num is not None and can_reserve_prev_chair and remain_chair > 0 :
            return True
        else:
            return False
        
    def clean_bad_chairs(self,):
        result = {}
        for key, subdict in self.chairs.items():
            # فرض می‌کنیم همه لیست‌ها طول یکسان دارند
            length = len(next(iter(subdict.values())))
            cleaned = {k: [] for k in subdict}
            for i in range(length):
                # اگر همه ویژگی‌ها None نبودن
                if all(subdict[attr][i] is not None for attr in subdict):
                    for attr in subdict:
                        cleaned[attr].append(subdict[attr][i])
            result[key] = cleaned
        self.chairs = result
        return self.chairs

    def select_chairs(self, sans_idx, max_reserve, min_price, start_chair, end_chair ):
        # self.go_to_sans_page(sans_idx)
        self.find_chairs()
        self.clean_bad_chairs()

        selected_chairs = []
        selected_chairs_dict:dict[str, dict[str, list]] = {}
        reserve_count = 0
        n = len(self.chairs)
        chairs_items = list(self.chairs.items())
        chairs_items.sort( key=lambda x: sum(x[1]['chairs_price']) / len(x[1]['chairs_price']), reverse=True)
        self.print_chairs(chairs_items)

        stop_loop = False
        for rn, rn_chairs in chairs_items:
            chairs_num = rn_chairs['chairs_num']
            chairs_x = rn_chairs['chairs_x']
            chairs_price = rn_chairs['chairs_price']
            chairs_reservable = rn_chairs['is_reservable']
            
            #------------------set chairs out of range reservable False----------------------
            # for k in range(len(chairs_num)):
            #     if not self.is_chair_in_range(chairs_num[k], start_chair, end_chair):
            #         chairs_reservable[k] = False

            if stop_loop:
                break

            i = 0
            while i < len(chairs_num):
                if not chairs_reservable[i]:
                    i+=1
                    continue
                if start_chair > 0 and chairs_num[i] < start_chair:
                    i+=1
                    continue
                if end_chair > 0 and chairs_num[i]> end_chair:
                    i+=1
                    continue
                chair = rn_chairs['chairs'][i]

                #is_last_chair = (max_reserve == (reserve_count + 1))
                remain_chair = max_reserve - reserve_count - 1

                if not self.check_single_chair_for_concert( idx=i,
                                               chairs_num=chairs_num,
                                               chairs_reservable=chairs_reservable,
                                               remain_chair=remain_chair,
                                               start_chair=start_chair,
                                               end_chair=end_chair):
                    i+=1
                    continue
                
                _rn_selected_chairs_num = []
                if rn in selected_chairs_dict:
                    _rn_selected_chairs_num = selected_chairs_dict[rn]['chairs_num']

                if not self.check_single_chair_for_myself(idx=i,
                                                          rn_selected_chairs_num=_rn_selected_chairs_num,
                                                          chairs_num=chairs_num,
                                                          chairs_reservable=chairs_reservable,
                                                          remain_chair=remain_chair,
                                                          start_chair=start_chair,
                                                          end_chair=end_chair):
                    chairs_reservable[i] = False
                    if remain_chair==0:
                        stop_loop = True
                        break
                    else:
                        i+=1
                        continue


                if self.safe_click(chair):
                    selected_chairs.append(chair)
                    reserve_count = self.get_reserve_count()
                    
                    if rn not in selected_chairs_dict:
                        selected_chairs_dict[rn] = {'chairs': [], 'chairs_num':[]}
                    selected_chairs_dict[rn]['chairs'].append(chair)
                    selected_chairs_dict[rn]['chairs_num'].append(chairs_num[i])

                

                if reserve_count == max_reserve :
                    return StatusCodes.SUCCESS
                i+=1
        if reserve_count > 0:
            return StatusCodes.SUCCESS
        return StatusCodes.NO_CHAIR_FOUND