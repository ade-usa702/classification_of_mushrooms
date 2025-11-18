from loguru import logger
import sys

FORMAT = "{time:DD.MM.YYYY  HH:mm:ss} | {level} |  {module}:{function}:{line} - {message}"
ROTATION = "5 MB"


def create_logger() -> "loguru.Logger":
    """Создание логгера """    
    logger.remove(0)
    logger.add("file.log", 
               rotation=ROTATION, 
               format=FORMAT)
    logger.add(sys.stdout,  
               format=FORMAT)
    return logger