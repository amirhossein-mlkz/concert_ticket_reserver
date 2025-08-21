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


class melotikWebScrepper(baseWebScrepper):

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

    def find_sans_buttons(self):
        super().find_sans_buttons()
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'خرید')]")
        print(f"Found {len(buttons)} reserve buttons.")
        self.sans_btns = buttons
        return self.sans_btns

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

    def click_and_decide(
        self,
        button_locator,
        success_marker_locator=None,
        max_wait_seconds=5,
        poll_ms=100
    ):
        """
        Clicks a button and quickly determines if:
        - Success: the input with id 'Mobile' is present
        - Error: toast message appeared
        - Unknown: no signal in the given time
        """
        # Wait for button to be clickable
        btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(button_locator)
        )
        self.safe_click(btn)

        # Wait until page is loaded after click
        WebDriverWait(self.driver, max_wait_seconds).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

        wait = WebDriverWait(self.driver, max_wait_seconds, poll_frequency=poll_ms / 1000.0)

        def first_signal(_):
            # Success: input with id 'Mobile' is present
            try:
                mobile_input = self.driver.find_element(By.ID, 'Mobile')
                if mobile_input.is_displayed():  # Check if the element is visible
                    return {'status': 'success', 'reason': 'mobile_input_present', 'error_text': None}
            except NoSuchElementException:
                pass  # If the element is not found, continue waiting

            # Error: toast container present
            toast_info = self.driver.execute_script("""
                const c = document.getElementById('toast-container');
                if (!c) return null;
                const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
                const items = Array.from(c.children || []).filter(el => visible(el));
                if (items.length === 0) return null;
                const text = items.map(el => (el.innerText || el.textContent || '').trim())
                                  .filter(t => t.length > 0)
                                  .join('\\n').trim();
                return text.length ? text : '';
            """)
            if toast_info is not None:
                return {'status': 'error', 'reason': 'toast_error', 'error_text': toast_info}

            return False  # keep waiting

        try:
            return wait.until(first_signal)
        except TimeoutException:
            return {'status': 'unknown', 'reason': 'timeout_no_signal', 'error_text': None}

    def find_chairs(self):
        # استفاده از JavaScript برای استخراج داده‌ها
        script = """
        let chairs = [];
        let chairElements = Array.from(document.querySelectorAll("g")).filter(chair => chair.classList.contains('active'));

        // پردازش هر صندلی
        chairElements.forEach(chair => {
            let rn = chair.getAttribute('rn');
            let c = chair.getAttribute('c');
            let p = chair.getAttribute('p');
            let x = chair.querySelector('rect') ? chair.querySelector('rect').getAttribute('x') : null;
            let g = chair.querySelector('rect') ? chair.querySelector('rect').getAttribute('data-group') : null;
            
            // بررسی اینکه فقط کلاس active وجود داشته باشد یا خیر
            let is_reservable = chair.classList.length === 1; // اگر تنها کلاس 'active' باشد، true است

            if (rn && c && p && x !== null) {
                chairs.push({
                    rn: rn,
                    c: parseInt(c),
                    price: parseInt(p),
                    x: parseFloat(x),
                    group: g,
                    is_reservable: is_reservable,  // تعیین وضعیت قابل رزرو بودن
                    element: chair
                });
            }
        });

        return chairs;
        """

        # اجرای اسکریپت جاوا اسکریپت برای استخراج داده‌ها از مرورگر
        chairs_data = self.driver.execute_script(script)

        self.chairs = {}

        # پردازش داده‌های دریافت شده
        for item in chairs_data:
            rn = item['rn']
            c = item['c']
            chair = item['element']
            x = item['x']
            p = item['price']
            group = item['group']
            is_reservable = item['is_reservable']

            rn = str(rn) + str(group)

            if rn not in self.chairs:
                self.chairs[rn] = {'chairs': [], 'chairs_num': [], 'chairs_x': [], 'chairs_price':[], 'is_reservable':[]}

            # افزودن صندلی به دیکشنری
            self.chairs[rn]['chairs'].append(chair)
            self.chairs[rn]['chairs_num'].append(c)
            self.chairs[rn]['chairs_x'].append(x)
            self.chairs[rn]['chairs_price'].append(p)
            self.chairs[rn]['is_reservable'].append(is_reservable)



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


    def reserve_chairs(self, user_info: dict):
        wait = WebDriverWait(self.driver, 20)
        name_input = wait.until(EC.presence_of_element_located((By.ID, "Name")))
        mobile_input = wait.until(EC.presence_of_element_located((By.ID, "Mobile")))
        family_input = wait.until(EC.presence_of_element_located((By.ID, "Family")))

        

        name_input.clear()
        mobile_input.clear()
        family_input.clear()


        name_input.send_keys(user_info.get("name", ""))
        mobile_input.send_keys(user_info.get("phone", ""))
        family_input.send_keys(user_info.get("family", ""))


    # ---------- Main Auto Reserve Flow ---------- #
    def get_reserve_count(self,):
        element = self.driver.find_element(By.ID, "selected_chairs_count_mobile")
        text_value = element.text 
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



                # if reserve_count == max_reserve or i==(n-1):
                #     #remove singles
                #     remove = True
                #     for select_rn , select_rn_chairs in selected_chairs_dict.items():
                #         rn_j = 0
                #         while rn_j<len(select_rn_chairs['chairs']):
                #             #check chair has at least one neighbor
                #             if (  select_rn_chairs['chairs_num'][rn_j]+1 in select_rn_chairs['chairs_num'] 
                #                 or select_rn_chairs['chairs_num'][rn_j]-1 in select_rn_chairs['chairs_num'] ):
                #                 rn_j+=1
                #                 continue
                #             chair = select_rn_chairs['chairs'][rn_j]
                #             self.safe_click(chair)
                #             selected_chairs.remove(chair)
                #             select_rn_chairs['chairs_num'].pop(rn_j)
                #             select_rn_chairs['chairs'].pop(rn_j)
                #             reserve_count-=1
                

                if reserve_count == max_reserve or i==(n-1):

                    result = self.click_and_decide(
                                    button_locator=(By.ID, "btnConfirmChairs"),
                                    success_marker_locator=(By.ID, "next-page-root"),
                                    max_wait_seconds=5,
                                    poll_ms=100
                                )

                    if result['status'] == 'success':
                        print("✅ Reservation confirmed:", result['reason'])
                        return StatusCodes.SUCCESS

                    elif result['status'] == 'error':
                        print("⚠ Error:", result['error_text'])
                        # Deselect one seat and try again
                        if selected_chairs:
                            for _ in range(10):
                                status = self.safe_click(selected_chairs[0])
                                if status:
                                    break
                                time.sleep(0.5)
                            selected_chairs.pop(-1)
                            reserve_count -= 1
                        # time.sleep(0.5)

                    else:
                        print("❓ Unknown:", result['reason'])
                        time.sleep(0.5)
                i+=1
        
        return StatusCodes.NO_CHAIR_FOUND
            


    def auto_reserve(self, url,sans_idx, user_info: dict, max_reserve=10, min_price=0, start_chair=-1, end_chair=-1):
        self.build()

        # Wait until at least one "خرید" button is found
        while True:
            self.go_to_url(url)
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
                status = self.select_chairs(idx, max_reserve, min_price, start_chair, end_chair)
            except Exception as e:
                print(e)
                time.sleep(0.5)
                self.driver.refresh()
                continue

            if status == StatusCodes.SUCCESS:
                self.reserve_chairs(user_info)
                return StatusCodes.SUCCESS

            idx+1


       
       

        return StatusCodes.NO_CHAIR_FOUND
