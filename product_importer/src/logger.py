import logging
from pathlib import Path
from datetime import datetime
import sys


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            self.log_dir = Path("logs")
            self.log_dir.mkdir(exist_ok=True)

            self.logger = logging.getLogger('ProductImporter')
            self.logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(
                self.log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log',
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            Logger._initialized = True

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls()
        return cls._instance.logger
