import logging
import sys
import pytest

from common.file import ROOT_PATH


@pytest.fixture(scope='session')
def setup_logging():
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('D://PycharmProjects/ds/log/api_test.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)

    return logger
