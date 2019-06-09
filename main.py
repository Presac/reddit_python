import yaml
import os
from reddit import CustomReddit


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
    else:
        config = init_config()
        redditors = init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    # Start the stream for checking new posts
    reddit.start_stream('FreeGameFindings', sites, redditors)


if __name__ == '__main__':
    main()
