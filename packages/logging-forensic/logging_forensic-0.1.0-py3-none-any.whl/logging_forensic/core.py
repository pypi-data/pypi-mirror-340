import logging
from pathlib import Path
from datetime import datetime

def forensic_logger(name: str,
                 logfile_path: Path = None,
                 level=logging.INFO,
                 console: bool = True,
                 timestamp: bool = True,
                 verbose: bool = False) -> logging.Logger:
    """
    create and setup a logger with path "../log/" and optional timestamp and console logging
    :param name: name of the logger
    :param logfile_path: path to log file
    :param level: logging level
    :param console: if true console logging
    :return: logger object
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    if logfile_path is None:
        base_path = Path.cwd() / 'log'
        base_path.mkdir(parents=True, exist_ok=True)

        timestring = datetime.now().strftime("%Y%m%d-%H%M%S") if timestamp else ''
        filename = f'{timestring}_{name}.log' if timestamp else f'{name}.log'
        logfile_path = base_path / filename
        if verbose:
            print(f'log file path: {logfile_path}')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        if verbose:
            print(f'creating logger {name}')
        file_handler = logging.FileHandler(logfile_path)
        file_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # optional console output
        if console:
            if verbose:
                print(f'creating console logger {name}')
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
    logger.propagate = False
    return logger
