import logging

def create_logger(logname='Trevor-Discord-Bot', default_level=logging.DEBUG, file_name=None, file_level=logging.INFO, format='%(name)s - %(asctime)s - %(levelname)s - %(message)s'):

    # Sets a default logger
    logger = logging.getLogger(logname)
    logger.setLevel(default_level)

    formatter = logging.Formatter(format)

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)

    logger.addHandler(stream_hander)
    
    if file_name is not None:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger