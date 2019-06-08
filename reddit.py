import praw
import time
import yaml


def find_last_x_posts(subreddit, amount):
    """Finds the newest posts in a subreddit."""
    new_python = subreddit.new(limit=amount)
    posts = []
    for submission in new_python:
        if not submission.stickied:
            posts.append({"title": submission.title,
                          "utl": submission.url,
                          "created": submission.created})
    return posts


def find_top_x_posts(subreddit, amount, sites):
    """Finds the top posts in a subreddit."""
    new_python = subreddit.top('week', limit=amount)
    posts = []
    for submission in new_python:
        if not submission.stickied:
            for site in sites:
                if site in submission.url.lower():
                    posts.append({"title": submission.title,
                                  "url": submission.url,
                                  "created": submission.created})
    return posts


def start_stream(subreddit, sites):
    """Starts a stream for a subreddit
    Any new post will be printed."""
    for submission in subreddit.stream.submissions(skip_existing=True):
        time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                    time.localtime(int(submission.created)))
        print('{}, URL: {}, CREATED: {}'.
              format(submission.title,
                     submission.url,
                     time_string))


def print_post(post):
    time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                time.localtime(int(post['created'])))
    print('{}, URL: {}, CREATED: {}'.
          format(post['title'],
                 post['url'],
                 time_string))


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


def main():
    # Open config file with passwords for the reddit client
    config = init_config()

    sites = init_sites_list()

    # Create the reddit client
    reddit = praw.Reddit(client_id=config['client_id'],
                         client_secret=config['client_secret'],
                         user_agent=config['user_agent'],
                         username=config['username'],
                         password=config['password'])

    # Set up the subreddit to check
    subreddit = reddit.subreddit('FreeGameFindings')

    # Start the stream for checking new posts
    # start_stream(subreddit, sites)
    posts = find_top_x_posts(subreddit, 20, sites)

    for post in posts:
        print_post(post)


if __name__ == '__main__':
    main()
