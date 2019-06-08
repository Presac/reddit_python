import praw
import time


class CustomReddit(object):
    def __init__(self, config, subreddit_name):
        self.reddit = praw.Reddit(client_id=config['client_id'],
                                  client_secret=config['client_secret'],
                                  user_agent=config['user_agent'],
                                  username=config['username'],
                                  password=config['password'])
        self.subreddit = self.reddit.subreddit(subreddit_name)

    def find_last_x_posts(self, amount):
        """Finds the newest posts in a subreddit."""
        new_python = self.subreddit.new(limit=amount)
        posts = []
        for post in new_python:
            if not post.stickied:
                posts.append({"title": post.title,
                              "utl": post.url,
                              "permalink": post.permalink,
                              "created": post.created})
        return posts

    def find_top_x_posts(self, amount, sites):
        """Finds the top posts in a subreddit."""
        new_python = self.subreddit.top('week', limit=amount)
        posts = []
        for post in new_python:
            if not post.stickied:
                for site in sites:
                    if site in post.url.lower():
                        posts.append({"title": post.title,
                                      "url": post.url,
                                      "permalink": post.permalink,
                                      "created": post.created})
        return posts

    def start_stream(self, sites, redditors):
        """Starts a stream for a subreddit
        Any new post will be printed."""
        posts = []
        for post in self.subreddit.stream.submissions(skip_existing=True):
            if not post.stickied:
                for site in sites:
                    if site in post.url.lower():
                        posts.append({"title": post.title,
                                      "url": post.url,
                                      "permalink": post.permalink,
                                      "created": post.created})

    @staticmethod
    def print_post(post):
        time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                    time.localtime(int(post['created'])))
        print('{}, URL: {}, CREATED: {}'.
              format(post['title'],
                     (post['url'] if len(post['url']) <= 50
                      else post['url'][:50] + "..."),
                     time_string))
