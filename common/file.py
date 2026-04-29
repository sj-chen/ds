import os
from configparser import ConfigParser
from typing import Any, Type, Dict, List, TypeVar
import yaml

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

def load_data(filename) :
    with open(os.path.join(ROOT_PATH,'data',filename), 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data

T = TypeVar('T')
def to_cases(cls: Type[T], raw: List[Dict[str, Any]]) -> List[T]:
    """通用转换器：将字典列表转换为指定 dataclass 的实例列表"""
    return [cls(**item) for item in raw]

