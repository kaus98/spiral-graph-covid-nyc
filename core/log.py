# https://gist.github.com/nguyenkims/e92df0f8bd49973f0c94bddf36ed7fd0
import logging
import sys
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


class MyLogger(Logger):
    def __init__(
            self,
            log_file=None,
            log_format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(filename)s - %(funcName)s - %(message)s",
            *args,
            **kwargs
    ):
        self.formatter = logging.Formatter(log_format)
        self.log_file = log_file

        Logger.__init__(self, log_file, *args, **kwargs)
        self.addHandler(self.get_console_handler())
        if log_file:
            self.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the| error up to parent
        self.propagate = False

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when="midnight")
        file_handler.setFormatter(self.formatter)
        return file_handler
