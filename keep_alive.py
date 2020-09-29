import time
import logging
from flask import Flask
from flask import request
from threading import Thread
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    logging.info(f'Ping received from {request.remote_addr}')
    
    status = subprocess.check_output(["systemctl", "is-active", "reddit_python.service"], universal_newlines=True).split('\n')
    return f'The reddit_python bot is {status}'

def run():
  app.run(host='0.0.0.0',port=1717)

def keep_alive():
    t = Thread(target=run)
    t.start()