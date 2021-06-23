import os
import inspect

class ProfilLogger:
    """Stop it, get some help"""

    def __init__(self, handlers):
        self.levels = {
            "debug": 10,
            "info": 20,
            "warning": 30,
            "error": 40,
            "critical": 50
        }
        self.log_level = "warning"
        self.handlers = handlers

    def set_log_level(self, level):
        if level in self.levels.keys():
            self.log_level = level

    def debug(self, msg):
        """Creates LogEntry with given msg, and passes it to the save method of every handler"""
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def info(self, msg):
        """Creates LogEntry with given msg, and passes it to the save method of every handler"""
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def warning(self, msg):
        """Creates LogEntry with given msg, and passes it to the save method of every handler"""
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def error(self, msg):
        """Creates LogEntry with given msg, and passes it to the save method of every handler"""
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def critical(self, msg):
        """Creates LogEntry with given msg, and passes it to the save method of every handler"""
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))


class FileHandler:
    """Used to save LogEntry to a .txt file"""
    def __init__(self, file_name="log.txt"):
        self.file_name = file_name

    def save(self, log_entry):
        """Saves given LogEntry to a txt file
        separates date, level, msg with ;
        if LogEntry.msg contains ; it is replaced with :"""

        log_entry.msg.replace(";", ":")
        with open (self.file_name, "a", newline="\n") as file:
            file.write(f"{log_entry.date} ; {log_entry.level} ; {log_entry.msg}\n")


class LogEntry:
    """Creates log entries"""
    def __init__(self, msg, level=None):
        from datetime import datetime
        self.msg = msg
        if level:
            self.level = level
        now = datetime.now()
        self.date = now.strftime("%b %d %Y %H:%M:%S")