import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    print("{} UTC {:+.0f} Ping Received".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.localtime().tm_gmtoff / 3600))
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()