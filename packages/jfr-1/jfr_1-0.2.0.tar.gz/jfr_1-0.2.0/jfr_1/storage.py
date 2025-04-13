# jfr_1/storage.py
import json
import os

STORAGE_PATH = os.path.join(os.path.dirname(__file__), "user_algorithms.json")

def load_all():
    if not os.path.exists(STORAGE_PATH):
        return []
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_all(data):
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
