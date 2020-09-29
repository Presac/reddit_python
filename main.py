#!/usr/bin/env python3

import os
import logging
from reddit import CustomReddit
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
    config = FI.init_config()
    redditors = FI.init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    # Start the stream for checking new posts
    reddit.start_stream(sub_name, sites, redditors)


if __name__ == '__main__':
    main()
