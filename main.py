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
    with open('redditors.yaml', 'r') as stream:
        try:
            redditors = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return redditors


def main():
    # Initialize information from files
    config = init_config()
    sites = init_sites_list()
    redditors = init_redditor_list()

    # Create the reddit client
    reddit = CustomReddit(config)

    # Start the stream for checking new posts
    reddit.start_stream('FreeGameFindings', sites, redditors)


if __name__ == '__main__':
    main()
