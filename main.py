import praw
import time
import yaml
from reddit import CustomReddit


def init_config():
    """Returns data from config.yaml"""
    with open('config.yaml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return config


def init_sites_list():
    """Returns a list of sites from a yaml file."""
    sites = []
    with open('sites.yaml', 'r') as stream:
        try:
            sites = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return sites


def init_redditor_list():
    """Returns a list of redditors from a yaml file."""
    redditors = []
    with open('sites.yaml', 'r') as stream:
        try:
            redditors = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return redditors


def message_to_redditor(reddit, name, message):
    reddit.redditor(name).message('', message)
    pass


def main():
    # Open config file with passwords for the reddit client
    config = init_config()

    sites = init_sites_list()

    # redditors = init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config, 'FreeGameFindings')

    # Start the stream for checking new posts
    # reddit.start_stream(subreddit, sites, redditors)

    posts = reddit.find_top_x_posts(20, sites)
    for post in posts:
        CustomReddit.print_post(post)


if __name__ == '__main__':
    main()
