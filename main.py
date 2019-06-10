import yaml
import os
from reddit import CustomReddit
from flask import Flask
import time
import requests
from threading import Timer, Thread
app = Flask(__name__)


def init_config():
    """Returns data from config.yaml"""
    with open('data/config.yaml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return config


def init_sites_list():
    """Returns a list of sites from a yaml file."""
    sites = []
    with open('data/sites.yaml', 'r') as stream:
        try:
            sites = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return sites


def init_redditor_list():
    """Returns a list of redditors from a yaml file."""
    redditors = []
    with open('data/redditors.yaml', 'r') as stream:
        try:
            redditors = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return redditors


def keep_alive():
    requests.get('http://localhost:5000')
    s = Timer(240.0, keep_alive)
    s.daemon = True
    s.start()


@app.route('/', methods=['GET'])
def hello():
    print("{} UTC {:+.0f} Ping Received"
          .format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                  time.localtime().tm_gmtoff / 3600))
    return 'All is good'


def main():
    place = os.environ.get('instance', None)

    # Initialize information from files
    sites = init_sites_list()
    if place is 'IS_GLITCH':
        config = {'client_id': os.environ.get('client_id', None),
                  'client_secret': os.environ.get('client_secret', None),
                  'user_agent': os.environ.get('user_agent', None),
                  'username': os.environ.get('username', None),
                  'password': os.environ.get('password', None)}
        redditors = [os.environ.get('redittors', None)]
        app.secret = os.environ.get('secret')
    else:
        config = init_config()
        redditors = init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    # Start the stream for checking new posts
    stream_thread = Thread(target=reddit.start_stream,
                           args=('FreeGameFindings',
                                 sites,
                                 redditors),
                           daemon=True)
    stream_thread.start()

    # Needed to keep the app alive on glitch.com
    keep_alive_timer = Timer(240.0, keep_alive)
    keep_alive_timer.daemon = True
    keep_alive_timer.start()

    app.run()


if __name__ == '__main__':
    main()
