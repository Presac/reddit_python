import praw
import time
import yaml


def find_last_posts(subreddit):
    new_python = subreddit.new(limit=3)

    for submission in new_python:
        if not submission.stickied:
            print('Title: {}, url: {}, created: {}'.
                  format(submission.title,
                         submission.url,
                         time.ctime(int(submission.created))))


# Open config file with passwords for the reddit client
with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Create the reddit client
reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     user_agent=config['user_agent'])

# Set up the subreddit to check
subreddit = reddit.subreddit('FreeGameFindings')

# Start the stream for checking new posts
for submission in subreddit.stream.submissions():
    time_string = time.strftime("%d-%m-%Y, %H:%M:%S",
                                time.localtime(int(submission.created)))
    print('{}, URL: {}, CREATED: {}'.
          format(submission.title,
                 submission.url,
                 time_string))
