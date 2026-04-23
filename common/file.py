import os
from configparser import ConfigParser
import yaml
import pytest


class MyConfigParser(ConfigParser):
    def __init__(self, defaults = None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_setting() -> dict:
    ini_path = os.path.join(ROOT_PATH, 'config','config.ini')
    config = MyConfigParser()
    config.read(ini_path, encoding='utf-8')
    data = {section: dict(config[section]) for section in config.sections()}
    return data

def load_data(filename) -> dict:
    with open(os.path.join(ROOT_PATH,'data',filename), 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data