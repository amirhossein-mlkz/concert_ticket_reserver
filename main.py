from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def reserve_ticket(event_url):
    # مسیر کروم‌درایور (باید دانلود شود)
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(event_url)
        driver.maximize_window()

        # منتظر بمان تا دکمه‌های رزرو لود شوند
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button[class*='reserve']")
        ))

        print(f"Found {len(buttons)} reserve buttons.")
        
        # روی اولین دکمه رزرو کلیک کن
        if buttons:
            buttons[0].click()
            print("Clicked on first reserve button.")
            time.sleep(2)  # کمی صبر برای بارگذاری صفحه بعد

        # اینجا می‌توانی ادامه مراحل رزرو را هم اضافه کنی
        # مثل انتخاب صندلی یا تایید سفارش

    except Exception as e:
        print("Error:", e)
    finally:
        time.sleep(5)  # برای مشاهده نتیجه
        driver.quit()

# اجرای تابع
link = input("Enter event link: ")
reserve_ticket(link)
