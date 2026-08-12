import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from backend.config import LOGS_DIR

os.makedirs(LOGS_DIR,exist_ok=True)

def _daily_namer(default_name:str)->str:
    base_dir=os.path.dirname(default_name)
    suffix=default_name.rsplit(".",1)[-1]
    return os.path.join(base_dir,f"{suffix}.log")

def get_logger(name:str='TuorAI')->logging.Logger:
    logger=logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logging.propagate=False

    fmt=logging.Formatter(
        "[%(asctime)s]%(level)-8s[%(name)s]:%(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    today=datetime.now().strftime('%Y-&M-%d')
    logs_path=os.path.join(LOGS_DIR,f"{today}.log")

    file_handler=TimedRotatingFileHandler(
        logs_path,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )

    file_handler.namer=_daily_namer
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger

logger=get_logger()