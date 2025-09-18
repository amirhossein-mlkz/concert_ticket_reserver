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

        chairs = [1,2,3,4]
        reservable = [False, False, True, True]

        self.check_single_chair_for_myself(1,[],  chairs, reservable, remain_chair=1)
        # self.check_single_chair_for_concert(1,  chairs, reservable, remain_chair=1)


    # ---------- Step 1: Find "خرید" buttons ---------- #

    # ---------- Step 1: Find "خرید" buttons ---------- #

    def find_sans_buttons(self):
        buttons = WebDriverWait(self.driver, 1).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'خرید')]"))
        )
                    
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

    def find_chairs(self, timeout=10):
        # استفاده از JavaScript برای استخراج داده‌ها
        try:
            # منتظر بمان تا حداقل یک صندلی active وجود داشته باشد
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "g.active"))
            )
        except Exception as e:
            print(f"Timeout: no active chairs found within {timeout} seconds. Error: {e}")
            return {}

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
        
        while True:
            try:
                status = self.select_chairs(idx, max_reserve, min_price, start_chair, end_chair)
                result = self.click_and_decide(
                                    button_locator=(By.ID, "btnConfirmChairs"),
                                    success_marker_locator=(By.ID, "next-page-root"),
                                    max_wait_seconds=5,
                                    poll_ms=100
                                )

                # if result['status'] == 'success':
                #     print("✅ Reservation confirmed:", result['reason'])
                #     return StatusCodes.SUCCESS

                if result['status'] == 'error':
                    print("⚠ Error:", result['error_text'])
                    # Deselect one seat and try again
                    self.driver.refresh()
                    continue



                # else:
                #     print("❓ Unknown:", result['reason'])
                #     time.sleep(0.5)
            except Exception as e:
                print(e)
                time.sleep(0.5)
                self.driver.refresh()
                continue

            if status == StatusCodes.SUCCESS:
                self.reserve_chairs(user_info)
                return StatusCodes.SUCCESS

            


       
       

        return StatusCodes.NO_CHAIR_FOUND
