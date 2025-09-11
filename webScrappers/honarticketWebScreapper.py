from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException,WebDriverException
import time

from webScrappers.baseWebScrepper import baseWebScrepper
from .StatusCodes import StatusCodes


class honarticketWebScreapper(baseWebScrepper):

    def __init__(self):
        super().__init__()
        self.chairs:dict[str,dict[str,list]] =  {}


    # ---------- Utility Helpers ---------- #

    def safe_click(self, element, scroll=True, use_js=True):
        """
        Attempts to click an element safely:
        - Scrolls into view
        - Normal Selenium click
        - JS click fallback if intercepted
        """
        try:
            # Wait until the element is visible and clickable
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
            
            # Scroll into view if required
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            
            # Attempt to click normally
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

    # ---------- Step 1: Find "خرید" buttons ---------- #

    def go_to_sans_page(self, idx):
        if len(self.sans_btns) > idx:
            self.safe_click(self.sans_btns[idx])

        #     WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.execute_script('return document.readyState') == 'complete'
        # )

        elements = WebDriverWait(self.driver, 20).until(
                lambda d: d.find_elements(By.TAG_NAME, "g") if len(d.find_elements(By.TAG_NAME, "g")) >= 30 else False
            )

    # ---------- Step 2: Click & Decide result ---------- #


    def _switch_to_frame_that_contains_hall(self, timeout=10):
        self.driver.switch_to.default_content()
        # اگر در همین زمینه بود
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "hall")))
            return
        except: pass
        # در iframe‌ها بگرد
        for f in self.driver.find_elements(By.TAG_NAME, "iframe"):
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(f)
            try:
                WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "hall")))
                return
            except:
                continue
        self.driver.switch_to.default_content()

    def find_chairs(self, timeout=10):
        # اطمینان از فریم درست + صبر تا DOM نهایی شود (کلاس‌ها اعمال شوند)
        self._switch_to_frame_that_contains_hall(timeout)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#hall .row div.chair"))
        )
        time.sleep(5)
        js = r"""
        const hall = document.getElementById('sectionTabs');
        if (!hall) return {};

        const rows = hall.querySelectorAll('.row');
        const res = {};

        rows.forEach(row => {
            const rn = row.id || '';
            // دقیقا همان شرط شما: div.chair که .reserved ندارد
            const divs = row.querySelectorAll('div.chair:not(.reserved)');
            if (!divs.length) return;

            const chairs = [];
            const chairs_input = [];
            const chairs_num = [];
            const chairs_x = [];
            const chairs_price = [];
            const is_reservable = [];

            divs.forEach(div => {
                const input = div.querySelector("input[name='chair']");
                if (!input) return;

                const txt = div.textContent || '';
                const m = txt.match(/\d+/);
                if (!m) return;
                const num = parseInt(m[0], 10);

                const price = parseInt(input.getAttribute("price"), 10);

                chairs.push(div);                              // WebElement
                chairs_num.push(num);
                chairs_input.push(input)
                chairs_x.push(-1);
                chairs_price.push(price);
                is_reservable.push(!(div.className||'').split(/\s+/).includes('pending'));
            });

            if (chairs.length) {
                res[rn] = { chairs,chairs_input, chairs_num, chairs_x, chairs_price, is_reservable };
            }
        });
        return res;
        """

        self.chairs = self.driver.execute_script(js)
        return self.chairs


    # ---------- Step 4: Fill User Form ---------- #
    def print_chairs(self, chair_items=None ):
        if chair_items is None:
            self.chairs.items()
        for rn, rn_chairs in chair_items:
            for i in range(len(rn_chairs['chairs_num'])):
                num = rn_chairs['chairs_num'][i]
                price = rn_chairs['chairs_price'][i]
                print(f"{rn} : {num} - {price}$")


    def get_reserve_count(self,):
        try:
            element = self.driver.find_element(By.ID, "chairs-count")
            text_value = element.text 
        except:
            return 0
        
        try:
            return int(text_value)
        except:
            return 0



    def select_chairs(self, sans_idx, max_reserve, min_price, start_chair, end_chair ):
        self.go_to_sans_page(sans_idx)
        self.find_chairs()
        selected_chairs = []
        selected_chairs_dict:dict[str, dict[str, list]] = {}
        reserve_count = 0
        n = len(self.chairs)
        chairs_items = list(self.chairs.items())
        chairs_items.sort( key=lambda x: sum(x[1]['chairs_price']) / len(x[1]['chairs_price']), reverse=True)

        self.print_chairs(chairs_items)
        for rn, rn_chairs in chairs_items:
            chairs_num = rn_chairs['chairs_num']
            chairs_x = rn_chairs['chairs_x']
            chairs_price = rn_chairs['chairs_price']
            chairs_reservable = rn_chairs['is_reservable']

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
                # prev_prev_prev_chair_reservable = chairs_reservable[i-3] if i>=3 else None
                # if reserve_count+1 == max_reserve:
                #     #DONT change prev beacuse we reserve it befor
                #     #prev_chair_reservable = False
                #     next_chair_reservable = False

                #     #prev_prev_chair_reservable = False
                #     next_next_chair_reservable = False

                # elif reserve_count+2 == max_reserve:
                #     #DONT change prev beacuse we reserve it befor
                #     #prev_prev_chair_reservable = False
                #     next_next_chair_reservable = False


                #in below comment *:not reservable    0:reservable  x:not exist or sold
                
                if max_reserve == reserve_count + 1:
                    #o*x
                    #oox
                    if  next_next_chair_num is None and next_chair_num is not None:
                        i+=2
                        continue
                    #o*o
                    if (    (next_chair_num is not None and not next_chair_reservable) 
                        and (next_next_chair_num is not None and next_next_chair_reservable)):
                        i+=2
                        continue
                    #oo*
                    if (    (next_chair_num is not None and next_chair_reservable)
                        and (next_next_chair_num is not None and not next_next_chair_reservable)
                        ):
                        i+=2
                        continue

                    
                
                #o*x        ->
                if next_chair_num is not None and not next_chair_reservable and next_next_chair_num is None:
                    i+=2
                    continue
                #x*o        <-
                if prev_chair_num is not None and not prev_chair_reservable and prev_prev_chair_num is None:
                    i+=2
                    continue
                #oo*X       ->
                if (    next_chair_num is not None and next_chair_reservable 
                    and next_next_chair_num is not None and not next_next_chair_reservable
                    and next_next_next_chair_num is None):
                    i+=2
                    continue
                
                #x*oo       <-
                if (    prev_chair_num is not None and prev_chair_reservable 
                    and prev_prev_chair_num is not None and not prev_prev_chair_reservable
                    and prev_prev_prev_chair_num is None):
                    i+=2
                    continue
                
                        
                
                if self.safe_click(chair):
                    selected_chairs.append(chair)
                    reserve_count = self.get_reserve_count()
                    
                    if rn not in selected_chairs_dict:
                        selected_chairs_dict[rn] = {'chairs': [], 'chairs_num':[]}
                    selected_chairs_dict[rn]['chairs'].append(chair)
                    selected_chairs_dict[rn]['chairs_num'].append(this_chair_num)

                
                if reserve_count == max_reserve or i==(n-1):

                    submit_btn = self.driver.find_element(By.ID, "btnSubmit") 
                    self.safe_click(submit_btn)
                    return StatusCodes.SUCCESS


                i+=1



    def check_accept_rules(self,):
        wait = WebDriverWait(self.driver, 20)
        checkbox = wait.until(EC.presence_of_element_located((By.ID, "chkRulesAccepted")))        
        if checkbox:
            if not checkbox.is_selected():
                checkbox.click()
        
        if checkbox.is_selected():
            return True
        else:
            return False
        
    def find_sans_buttons(self, timeout=5):
        wait = WebDriverWait(self.driver, timeout)

        sans_container = wait.until(
            EC.presence_of_element_located((By.ID, "showTimesMenu"))
        )

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#showTimesMenu a"))
        )

        sans_containers = self.driver.find_element(By.ID, "showTimesMenu")        
        sans = sans_containers.find_elements(By.CSS_SELECTOR, "a:not(.disabled)")
        print(f"Found {len(sans)} reserve buttons.")
        self.sans_btns = sans
        return self.sans_btns

    def go_to_sans_page(self, idx):
        if len(self.sans_btns) > idx:
            self.safe_click(self.sans_btns[idx])

      
            


    def auto_reserve(self, url,sans_idx, user_info: dict, max_reserve=10, min_price=0, start_chair=-1, end_chair=-1):
        self.build()
        while True:
            self.go_to_url(url)
            self.check_accept_rules()
            self.find_sans_buttons()
            if len(self.sans_btns) == 0:
                time.sleep(0.5)
            else:
                break

        idx = sans_idx - 1
        if idx> (len(self.sans_btns) -1):
            return StatusCodes.NO_SANS_FOUND
    

        while idx < len(self.sans_btns):
            try:
                status = self.select_chairs(idx, max_reserve, min_price, start_chair=start_chair, end_chair=end_chair)
        
            except Exception as e:
                print(e)
                time.sleep(0.5)
                self.driver.refresh()
                continue


            if status == StatusCodes.SUCCESS:
                self.reserve_chairs(user_info)
                return StatusCodes.SUCCESS
        

    def reserve_chairs(self, user_info: dict):
        wait = WebDriverWait(self.driver, 20)
        name_input = wait.until(EC.presence_of_element_located((By.NAME, "userFName")))
        mobile_input = wait.until(EC.presence_of_element_located((By.NAME, "userMobile")))
        family_input = wait.until(EC.presence_of_element_located((By.NAME, "userLName")))

        

        name_input.clear()
        mobile_input.clear()
        family_input.clear()


        name_input.send_keys(user_info.get("name", ""))
        mobile_input.send_keys(user_info.get("phone", ""))
        family_input.send_keys(user_info.get("family", ""))