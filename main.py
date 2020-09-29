#!/usr/bin/env python3

import os
from reddit import CustomReddit
from file_import import file_importing as FI

sub_name = 'FreeGameFindings'

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
