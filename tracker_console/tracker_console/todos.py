import logging
from tracker_console.args_parser import ArgsParser


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def main():
    setup_logger('logger', 'logs.log')

    args_parser = ArgsParser()
    args_parser.command_execute()


if __name__ == '__main__':
    main()