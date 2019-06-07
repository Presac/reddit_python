import praw
import time
import yaml

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for data in config:
    print('key: {}, value: {}'.format(data, config[data]))


reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     user_agent=config['user_agent'])

subreddit = reddit.subreddit('FreeGameFindings')
for submission in subreddit.stream.submissions():
    print('Title: {}, url: {}, created: {}'.
          format(submission.title,
                 submission.url,
                 time.ctime(int(submission.created))))


# new_python = subreddit.new(limit=3)

# for submission in new_python:
#     if not submission.stickied:
#         print('Title: {}, url: {}, created: {}'.
#               format(submission.title,
#                      submission.url,
#                      time.ctime(int(submission.created))))
