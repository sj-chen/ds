import pytest
import logging
import sys
from pathlib import Path
from datetime import datetime

@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / "log"
    LOG_DIR.mkdir(exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"api_test_{today_str}.log"
    log_path = LOG_DIR / log_filename

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    def configure_library_logger(name):
        lib_logger = logging.getLogger(name)
        lib_logger.setLevel(logging.DEBUG)
        lib_logger.propagate = False
        # 清理原有 handler，避免 pytest 内置 handler 干扰
        for h in lib_logger.handlers[:]:
            lib_logger.removeHandler(h)
        lib_logger.addHandler(file_handler)
        lib_logger.addHandler(console_handler)
        return lib_logger

    configure_library_logger('urllib3')
    configure_library_logger('pymysql')

    # 业务 logger
    test_logger = logging.getLogger('api_test')
    test_logger.setLevel(logging.DEBUG)
    test_logger.propagate = False
    for h in test_logger.handlers[:]:
        test_logger.removeHandler(h)
    test_logger.addHandler(file_handler)
    test_logger.addHandler(console_handler)

    return test_logger

@pytest.fixture(scope='session', autouse=True)
def setup_logging2():
    BASE_DIR = Path(__file__).resolve().parent.parent  # BaseApi 的上层目录
    LOG_DIR = BASE_DIR / "log"
    LOG_DIR.mkdir(exist_ok=True)  # 确保目录存在
    # 2. 生成带日期的文件名，例如 api_test_2026-04-24.log
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"api_test_{today_str}.log"
    log_path = LOG_DIR / log_filename
    #urllib3.history
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.DEBUG)

    #pymysql
    logging.basicConfig(level=logging.DEBUG)  # 或者把 pymysql 的 logger 单独设
    logger = logging.getLogger("pymysql")
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
