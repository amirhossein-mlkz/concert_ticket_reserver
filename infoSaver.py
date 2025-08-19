import json
import os

class infoSaver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data: dict):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self) -> dict:
        if not os.path.exists(self.file_path):
            return {} 
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)
