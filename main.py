#!/usr/bin/env python3

import os
import logging
from reddit import CustomReddit
from threading import Thread
from keep_alive import keep_alive
from file_import import file_importing as FI

sub_name = 'FreeGameFindings'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('reddit.log'),
        logging.StreamHandler()
    ])

def main():
    place = os.environ.get('instance', None)

    # Initialize information from files
    sites = FI.init_sites_list()
    if place == 'IS_REPL':
        config = {'client_id': os.environ.get('client_id', None),
                  'client_secret': os.environ.get('client_secret', None),
                  'user_agent': os.environ.get('user_agent', None),
                  'username': os.environ.get('username', None),
                  'password': os.environ.get('password', None)}
        redditors = [os.environ.get('redditors', None)]
    else:
        config = FI.init_config()
        redditors = FI.init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    stream_thread = Thread(target=reddit.start_stream,
                            args=(sub_name, sites, redditors),
                            daemon=True)
    stream_thread.start()

    keep_alive()


if __name__ == '__main__':
    main()
