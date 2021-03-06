import yaml

class FileImporting(object):
    @staticmethod
    def init_config():
        """Returns data from config.yaml"""
        with open('data/config.yaml', 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                config = ''

        return config

    @staticmethod
    def init_sites_list():
        """Returns a list of sites from a yaml file."""
        sites = []
        with open('data/sites.yaml', 'r') as stream:
            try:
                sites = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        return sites

    @staticmethod
    def init_redditor_list():
        """Returns a list of redditors from a yaml file."""
        redditors = []
        with open('data/redditors.yaml', 'r') as stream:
            try:
                redditors = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        return redditors
