import os
import time
import requests
from reddit import CustomReddit
from file_import import file_importing as FI
from threading import Timer, Thread
from flask import Flask

app = Flask(__name__)
sub_name = 'FreeGameFindings'
domain = 'http://{}.glitch.me/'.format(os.environ.get('PROJECT_DOMAIN'), None)


def keep_alive():
    requests.get(domain)
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
    sites = FI.init_sites_list()
    if place is 'IS_GLITCH':
        config = {'client_id': os.environ.get('client_id', None),
                  'client_secret': os.environ.get('client_secret', None),
                  'user_agent': os.environ.get('user_agent', None),
                  'username': os.environ.get('username', None),
                  'password': os.environ.get('password', None)}
        redditors = os.environ.get('redittors', None)
        app.secret = os.environ.get('secret')
    else:
        config = FI.init_config()
        redditors = FI.init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    if place is 'IS_GLITCH':
        # Start the stream for checking new posts
        stream_thread = Thread(target=reddit.start_stream,
                               args=(sub_name, sites, redditors),
                               daemon=True)
        stream_thread.start()

        # Needed to keep the app alive on glitch.com
        keep_alive_timer = Timer(240.0, keep_alive)
        keep_alive_timer.daemon = True
        keep_alive_timer.start()

        app.run()
    else:
        reddit.start_stream(sub_name, sites, redditors)


if __name__ == '__main__':
    main()
