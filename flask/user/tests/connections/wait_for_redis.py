import os
import time

from config import config
from src.databases.cache import cache

if __name__ == "__main__":
    while True:
        if cache.ping():
            print("WAIT FOR CACHE ...")
            break
        time.sleep(1)
