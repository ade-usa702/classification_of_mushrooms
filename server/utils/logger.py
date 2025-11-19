from loguru import logger
import sys
import os

FORMAT = "{time:DD.MM.YYYY  HH:mm:ss} | {level} |  {module}:{function}:{line} - {message}"
ROTATION = "5 MB"
FILENAME = os.path.abspath("file.log")


def create_logger() -> "loguru.Logger":
    """Создание логгера """    
    logger.remove(0)
    logger.add(FILENAME, 
               rotation=ROTATION, 
               format=FORMAT)
    logger.add(sys.stdout,  
               format=FORMAT)
    return logger


log = create_logger()