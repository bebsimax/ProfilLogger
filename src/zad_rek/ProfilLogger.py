import os
import inspect

class ProfilLogger:
    """Stop it, get some help"""

    def __init__(self):
        self.levels = {
            "info": 20,
            "warning": 30
        }
        self.log_level = "warning"

    def info(self, msg):
        """Creates info log with specified message in log.log file"""
        method_name = inspect.currentframe().f_code.co_name
        file = open("log.log", "a")
        if self.levels[method_name] >= self.levels[self.log_level]:
            file.write(msg + '\n')
        file.close()


    def set_log_level(self, level):
        if level in self.levels.keys():
            self.log_level = level


    def warning(self, msg):
        """Creates warning log with specified message in log.log file"""
        method_name = inspect.currentframe().f_code.co_name
        file = open("log.log", "a")
        if self.levels[method_name] >= self.levels[self.log_level]:
            file.write(msg + '\n')
        file.close()
