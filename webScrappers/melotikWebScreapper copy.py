from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from webScrappers.baseWebScrepper import baseWebScrepper
from .StatusCodes import StatusCodes


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class melotikWebScrepper(baseWebScrepper):

    def __init__(self):
        super().__init__()
        

    # ---------- Utility Helpers ---------- #

    def safe_click(self, element, scroll=True, use_js=True):
        try:
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            return True
        except ElementClickInterceptedException:
            if use_js:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            return False
        except Exception:
            return False

    def get_chair_position(self, chair):
        position = self.driver.execute_script("""
            var el = arguments[0];
            var rect = el.getBoundingClientRect();
            return {x: rect.left, y: rect.top};
        """, chair)
        return position['x'], position['y']

    def get_middle_chairs(self):
        middle_chairs = []
        middle_x = self.get_middle_x()
        for chair in self.chairs:
            x, y = self.get_chair_position(chair)
            if abs(x - middle_x) < 10:
                middle_chairs.append(chair)
        return middle_chairs

    def get_middle_x(self):
        return 500  # Replace with actual logic to calculate center position

    def is_single_chair(self, chair):
        adjacent_chairs = self.get_adjacent_chairs(chair)
        return len(adjacent_chairs) == 0

    def get_adjacent_chairs(self, chair):
        x, y = self.get_chair_position(chair)
        adjacent_chairs = []
        
        for other_chair in self.chairs:
            other_x, other_y = self.get_chair_position(other_chair)
            if (abs(x - other_x) <= 1 and abs(y - other_y) <= 1):
                adjacent_chairs.append(other_chair)

        return adjacent_chairs

    def select_chairs(self, sans_idx, max_reserve):
        self.goto(sans_idx)
        self.find_active_chairs()

        selected_chairs = []
        reserve_count = 0
        n = len(self.chairs)
        
        # Step 1: First, prioritize selecting middle chairs
        middle_chairs = self.get_middle_chairs()
        
        for chair in middle_chairs:
            if self.safe_click(chair):
                selected_chairs.append(chair)
                reserve_count += 1
            if reserve_count == max_reserve:
                break

        # Step 2: Then, select side chairs to avoid single chair problem
        for i, chair in enumerate(self.chairs):
            if chair not in selected_chairs:
                # Ensure selecting the chair does not create a single chair
                if not self.is_single_chair(chair):
                    if self.safe_click(chair):
                        selected_chairs.append(chair)
                        reserve_count += 1
                else:
                    # If it's a single chair, select its adjacent chair to avoid a single chair
                    adjacent_chairs = self.get_adjacent_chairs(chair)
                    for adj_chair in adjacent_chairs:
                        if adj_chair not in selected_chairs:
                            if self.safe_click(adj_chair):
                                selected_chairs.append(adj_chair)
                                reserve_count += 1
                            break

            # Stop if max_reserve has been reached
            if reserve_count == max_reserve:
                break
        
        # Ensure the number of selected chairs doesn't exceed max_reserve
        if reserve_count > max_reserve:
            print(f"Error: Selected chairs exceed max reserve limit. Currently selected: {reserve_count}")
            while reserve_count > max_reserve:
                chair_to_deselect = selected_chairs.pop()  # Remove last selected chair
                self.safe_click(chair_to_deselect)  # Deselect it
                reserve_count -= 1
                print(f"Deselected chair. Remaining selected: {reserve_count}")

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
            if selected_chairs:
                for _ in range(10):
                    status = self.safe_click(selected_chairs[0])
                    if status:
                        break
                    time.sleep(0.5)
                selected_chairs.pop(0)
            time.sleep(0.5)
        else:
            print("❓ Unknown:", result['reason'])
            time.sleep(0.5)

        return StatusCodes.NO_CHAIR_FOUND

    def find_active_chairs(self):
        def enough_g_tags(drv):
            elements = drv.find_elements(By.XPATH, "//*[local-name()='g']")
            return len(elements) >= 5

        WebDriverWait(self.driver, 20).until(enough_g_tags)

        chairs = self.driver.find_elements(
            By.XPATH, "//*[local-name()='g' and @class='active']"
        )
        self.chairs = chairs
        return chairs

    def reserve_chairs(self, user_info: dict):
        wait = WebDriverWait(self.driver, 20)
        name_input = wait.until(EC.presence_of_element_located((By.ID, "Name")))
        mobile_input = wait.until(EC.presence_of_element_located((By.ID, "Mobile")))

        name_input.clear()
        mobile_input.clear()

        name_input.send_keys(user_info.get("name", ""))
        mobile_input.send_keys(user_info.get("phone", ""))

    def auto_reserve(self, url, user_info: dict, max_reserve=10):
        self.build()

        while True:
            self.go_to_url(url)
            self.find_sans_buttons()
            if len(self.sans_btns) == 0:
                time.sleep(1)
            else:
                break
        
        idx = 0
        while idx < len(self.sans_btns):
            try:
                status = self.select_chairs(idx, max_reserve)
            except:
                continue

            if status == StatusCodes.SUCCESS:
                self.reserve_chairs(user_info)
                break

            idx += 1
        
        return StatusCodes.NO_CHAIR_FOUND
