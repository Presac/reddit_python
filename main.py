import os
import requests
from reddit import CustomReddit
from threading import Thread
from keep_alive import keep_alive
from file_import import file_importing as FI

sub_name = 'FreeGameFindings'

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

    if place == 'IS_REPL':
        # Start the stream for checking new posts
        stream_thread = Thread(target=reddit.start_stream,
                               args=(sub_name, sites, redditors),
                               daemon=True)
        stream_thread.start()

        keep_alive()
    else:
        reddit.start_stream(sub_name, sites, redditors)


if __name__ == '__main__':
    main()
