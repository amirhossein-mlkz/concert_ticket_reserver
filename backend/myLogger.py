import os
import threading
import logging
import jdatetime  # pip install jdatetime

LOG_SEPRATOR = '_'*100

class myLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(myLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, path='logs'):
        if not hasattr(self, "initialized"):  # فقط یک بار اجرا شود
            self.initialized = True
            self.path = path

            # نام پوشه بر اساس تاریخ و ساعت شمسی
            now_jalali = jdatetime.datetime.now()
            folder_name = now_jalali.strftime("%Y-%m-%d_%H-%M-%S")
            self.log_dir = os.path.join(os.getcwd(), self.path, folder_name)
            os.makedirs(self.log_dir, exist_ok=True)

            log_file = os.path.join(self.log_dir, "app.log")

            # تنظیم logging
            self.logger = logging.getLogger("AppLogger")
            self.logger.setLevel(logging.DEBUG)

            # فرمت زمان با تاریخ شمسی
            class JalaliFormatter(logging.Formatter):
                def formatTime(self, record, datefmt=None):
                    t = jdatetime.datetime.fromtimestamp(record.created)
                    if datefmt:
                        return t.strftime(datefmt)
                    return t.strftime("%Y-%m-%d %H:%M:%S")

            formatter = JalaliFormatter("[%(asctime)s] [%(levelname)s] %(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")

            # File Handler
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger