# encoding: utf-8
import logging
import os
from pathlib import Path


class LoggerMixin:
    """
    Mixin class that provides logging functionality to classes.
    Mimics Ruby's Spider::Logger module.
    """

    @property
    def logger_file(self):
        """Generate log file path based on class name"""
        log_dir = Path(__file__).parent.parent / "log"
        log_dir.mkdir(exist_ok=True)

        if self.__class__.__name__ != 'object':
            # Convert CamelCase to snake_case
            class_name = self.__class__.__name__
            snake_case = ''.join(['_' + c.lower() if c.isupper() else c for c in class_name]).lstrip('_')
            file_name = f"{snake_case}.log"
        else:
            # For module-level usage
            from spider.utils.optparse import SpiderOptions
            script_name = os.path.basename(__file__)
            file_name = f"{script_name}_{SpiderOptions['name']}.log"

        return log_dir / file_name

    @property
    def logger(self):
        """Get or create logger instance"""
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
            self._logger.setLevel(logging.DEBUG)

            # Remove existing handlers
            self._logger.handlers = []

            # Create file handler
            handler = logging.FileHandler(self.logger_file, encoding='utf-8')
            handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)

            self._logger.addHandler(handler)

        return self._logger


def get_logger(name):
    """
    Get a standalone logger (for use in scripts that don't have classes)

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger instance
    """
    log_dir = Path(__file__).parent.parent / "log"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create file handler
    from spider.utils.optparse import SpiderOptions
    log_file = log_dir / f"run_{SpiderOptions['name']}.log"
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
