import logging
from flask import Flask
from flask import request
from threading import Thread
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    logging.info(f'Ping received from {request.remote_addr}')
    
    status = []
    for command in ["ActiveState", "SubState"]:
        status.append(subprocess.check_output(["systemctl", "show", "-p", command, "--value", "reddit_python.service"], universal_newlines=True).split('\n')[0])

    return f'The reddit_python bot is {status[0]} and {status[1]}'

def run():
    app.run(host='0.0.0.0', port=59246)

def keep_alive():
    t = Thread(target=run)
    t.start()


if __name__ == '__main__':
    run()