import praw
import time


class CustomReddit(object):
    def __init__(self, config):
        self.reddit = praw.Reddit(client_id=config['client_id'],
                                  client_secret=config['client_secret'],
                                  user_agent=config['user_agent'],
                                  username=config['username'],
                                  password=config['password'])

    def find_last_x_posts(self, sub, amount):
        """Finds the newest posts in a subreddit."""
        new_python = self.reddit.subreddit(sub).new(limit=amount)
        posts = []
        for post in new_python:
            if not post.stickied:
                posts.append({"title": post.title,
                              "utl": post.url,
                              "permalink": post.permalink,
                              "created": post.created})
        return posts

    def find_top_x_posts(self, sub, amount, sites):
        """Finds the top posts in a subreddit."""
        new_python = self.reddit.subreddit(sub).top('week', limit=amount)
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

    def start_stream(self, sub, sites, redditors):
        """Starts a stream for a subreddit
        Any new post will be printed."""
        '''for redditor in redditors:
            self.message_to_redditor(redditor,
                                     'The app for new posts has started.')'''
        print('Started streaming from ' + sub)
        for post in self.reddit.subreddit(sub).stream.submissions():
            # if any(site in post.url.lower() for site in sites):
            for site in sites:
                if site in post.url.lower():
                    post_info = {"title": post.title,
                                 "url": post.url,
                                 "permalink": post.permalink,
                                 "created": post.created}
                    # self.print_post(post_info)
                    for redditor in redditors:
                        # print(redditor)
                        self.message_to_redditor(redditor, site, post.permalink)

    def message_to_redditor(self, name, subject, message):
        self.reddit.redditor(name).message(subject, message)

    @staticmethod
    def print_post(post):
        time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                    time.localtime(int(post['created'])))
        print('{}, URL: {}, CREATED: {}'.
              format(post['title'],
                     (post['url'] if len(post['url']) <= 50
                      else post['url'][:50] + "..."),
                     time_string))
