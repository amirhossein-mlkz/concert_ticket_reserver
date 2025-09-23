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
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "hall")))
            return
        except: pass
        # در iframe‌ها بگرد
        for f in self.driver.find_elements(By.TAG_NAME, "iframe"):
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(f)
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "hall")))
                return
            except:
                continue
        self.driver.switch_to.default_content()


    def wait_for_chairs_update(self, timeout=10):
        def chairs_ready(driver):
            chairs = driver.find_elements(By.CSS_SELECTOR, "#hall div.row div.chair")
            # حداقل یکی reserved یا pending شده باشه
            return any(
                "reserved" in (c.get_attribute("class") or "") or
                "pending" in (c.get_attribute("class") or "")
                for c in chairs
            )
        WebDriverWait(self.driver, timeout).until(chairs_ready)

    def find_chairs(self, timeout=10):
        # اطمینان از فریم درست + صبر تا DOM نهایی شود (کلاس‌ها اعمال شوند)
        self._switch_to_frame_that_contains_hall(timeout)
 

        WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#hall div.row div.chair"))
        )

        self.wait_for_chairs_update(timeout)

        js = r"""
       let main_hall;

        const hall = document.getElementById('sectionTabs');

        if (!hall) {
            main_hall = document.getElementById('hall');
        } else {
            main_hall = hall.querySelector("div");
        }

        

        if (!main_hall) return {};


        const rows = main_hall.querySelectorAll('.row');
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

      
    def click_submit_btn(self,):
        submit_btn = self.driver.find_element(By.ID, "btnSubmit") 
        self.safe_click(submit_btn)

        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.any_of(
                    EC.visibility_of_element_located((By.NAME, "userFName")),  # فقط اگر قابل مشاهده باشد
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.block.notify"))
                )
            )
            # بررسی اینکه کدام ظاهر شده
            if element.get_attribute("name") == "userFName":
                return True, element
            else:
                return False, element

        except Exception as e:
            print("Timeout! هیچ کدام پیدا نشد.")
            return False, None
        
    def close_reserve_error(self, error_element):
        a_element = error_element.find_element(By.TAG_NAME, "a")
        if not self.safe_click(a_element):
            time.sleep(0.5)
            self.close_reserve_error(error_element)



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
                ret, element = self.click_submit_btn()
                if element is None:
                    self.auto_reserve(url, sans_idx, user_info, max_reserve, min_price, start_chair, end_chair)
                    return

                if not ret:
                    self.close_reserve_error(element)
                else:
                    self.reserve_chairs(user_info)
                    return StatusCodes.SUCCESS
        

    def reserve_chairs(self, user_info: dict):
        wait = WebDriverWait(self.driver, 20)
        time.sleep(1)
        name_input = wait.until(EC.presence_of_element_located((By.NAME, "userFName")))
        mobile_input = wait.until(EC.presence_of_element_located((By.NAME, "userMobile")))
        family_input = wait.until(EC.presence_of_element_located((By.NAME, "userLName")))

        

        name_input.clear()
        mobile_input.clear()
        family_input.clear()


        name_input.send_keys(user_info.get("name", ""))
        mobile_input.send_keys(user_info.get("phone", ""))
        family_input.send_keys(user_info.get("family", ""))