import wget
import os
import time

url = 'https://raw.githubusercontent.com/gg64du02/bomberman-by-not-sure/dev-multicast-lan/bomberman-main.py'

while(True):
    time.sleep(10)
    os.remove("bomberman-main.py")
    filename = wget.download(url)
