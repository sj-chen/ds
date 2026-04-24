import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pytest



@pytest.fixture(scope='session')
def setup_logging():
    BASE_DIR = Path(__file__).resolve().parent.parent  # BaseApi 的上层目录
    LOG_DIR = BASE_DIR / "log"
    LOG_DIR.mkdir(exist_ok=True)  # 确保目录存在
    # 2. 生成带日期的文件名，例如 api_test_2026-04-24.log
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"api_test_{today_str}.log"
    log_path = LOG_DIR / log_filename

    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)

    return logger
