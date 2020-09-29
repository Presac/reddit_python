import praw
import time
import logging
from typing import List
from prawcore.exceptions import PrawcoreException


class CustomReddit(object):
    def __init__(self, config: dict):
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
            username=config['username'],
            password=config['password']
        )

    def find_last_x_posts(self, sub: str, amount: int) -> List[dict]:
        """Finds the newest posts in a subreddit

        Args:
            sub (str): The name of the subreddit to get submissions from
            amount (int): The amount of submissions to search

        Returns:
            List[dict]: A list of dicts containing information about submissions
        """                
        new_python = self.reddit.subreddit(sub).new(limit=amount)
        posts = []
        for post in new_python:
            if not post.stickied:
                posts.append({"title": post.title,
                              "url": post.url,
                              "permalink": post.permalink,
                              "created": post.created})
        return posts

    def find_top_x_posts(self, sub: str, amount: int, sites: List[str] = None) -> List[dict]:
        """Finds the top posts in a subreddit

        Args:
            sub (str): The name of the subreddit to get submissions from
            amount (int): The amount of submissions to search
            sites (List[str], optional): A list of strings to search for in the submission urls. Defaults to None.

        Returns:
            List[dict]: A list of dicts containing information about submissions
        """        
        new_python = self.reddit.subreddit(sub).top('week', limit=amount)
        posts = []
        for post in new_python:
            if not post.stickied:
                if sites != None:
                    if not any(site in post.url.lower() for site in sites):
                        continue

                posts.append({
                    "title": post.title,
                    "url": post.url,
                    "permalink": post.permalink,
                    "created": post.created})
        return posts

    def start_stream(self, sub: str, redditors: List[str], sites: List[str] = None):
        """Starts a stream for a subreddit to get any new submissions

        Args:
            sub (str): The name of the subreddit to stream from 
            redditors (List[str]): A list of redditors to send updates to
            sites (List[str], optional): A list of strings to search for in the submission urls. Defaults to None.
        """        
        logging.info(f'Starting stream from {sub}')

        running = True
        while running:
            try:
                sub_stream = self.reddit.subreddit(sub).stream \
                        .submissions(skip_existing=True)

                for post in sub_stream:
                    if sites != None:
                        if not any(site in post.url.lower() for site in sites):
                            continue
                    
                    logging.info(f'New game: {post.permalink}')
                    logging.info(f'Sending info to: {redditors}')

                    message = f'[{post.title}]({post.permalink})'
                    
                    for redditor in redditors:
                        self.send_message(redditor, 'New Game', message)
            except KeyboardInterrupt:
                logging.info('Termination received')
                running = False
            except PrawcoreException:
                logging.exception('run loop')
                time.sleep(10)

    def send_message(self, name: str, subject: str, message: str):
        """Sends a message to a redditor

        Args:
            name (str): The name of the redditor
            subject (str): The subject of the message
            message (str): The message to send
        """
        self.reddit.redditor(name).message(subject, message)

    @staticmethod
    def print_post(post: dict):
        time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                    time.localtime(int(post['created'])))
        print('{}, URL: {}, CREATED: {}'.
              format(post['title'],
                     (post['url'] if len(post['url']) <= 50
                      else post['url'][:50] + "..."),
                     time_string))
