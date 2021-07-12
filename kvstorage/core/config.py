import json
import yaml


class ConfigLoaderException(Exception):
    pass


class ConfigLoader:
    def __init__(self, parser):
        self.config_parser = parser

    def load_config(self):
        conf = self.config_parser.parse_config()
        return conf


class JSONParser:
    def __init__(self, path):
        self.config_file = path

    def parse_config(self):
        with open(self.config_file, "r") as conf:
            try:
                conf_data = json.load(conf)
            except json.decoder.JSONDecodeError:
                raise ConfigLoaderException(
                    "Cant' parse config: {}".format(self.config_file)
                )
        return conf_data


class YAMLParser:
    def __init__(self, path):
        self.config_file = path

    def parse_config(self):
        with open(self.config_file, "r") as conf:
            try:
                conf_data = yaml.load(conf)
            except yaml.YAMLError:
                raise ConfigLoaderException(
                    "Cant' parse config: {}".format(self.config_file)
                )
        return conf_data
