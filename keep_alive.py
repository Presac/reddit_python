import time
from flask import Flask
from threading import Thread
import subprocess

app = Flask('')

@app.route('/')
def home():
    print("{} UTC {:+.0f} Ping Received".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.localtime().tm_gmtoff / 3600))
    
    status = subprocess.check_output(["systemctl", "is-active", "reddit_python.service"], universal_newlines=True).split('\n')
    return f'The reddit_python bot is {status}'

def run():
  app.run(host='0.0.0.0',port=1717)

def keep_alive():  
    t = Thread(target=run)
    t.start()