import wget
import os
import time

url = 'https://raw.githubusercontent.com/gg64du02/bomberman-by-not-sure/blob/master/bomberman-main.py'

# while(True):
#     time.sleep(10)
os.remove("bomberman-main.py")
filename = wget.download(url)
