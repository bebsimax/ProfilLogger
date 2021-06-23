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

    def __repr__(self):
        return f"ProfiLogger(handlers={self.handlers})"

    def __str__(self):
        return self.handlers

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

    def __new__(cls, entry="log.txt"):

        if entry == "log.txt":
            return super(FileHandler, cls).__new__(cls)

        if not isinstance(entry, str):
            raise TypeError("Input should be a string")

        if len(entry) <= 4:
            raise ValueError("File name must be at least 5 characters long and include .txt at the end")

        if len(entry) >= 60:
            raise ValueError("Length of file name cannot get past 60 characters")

        if entry[-4:] != ".txt":
            raise ValueError("Passed file name does not end with '.txt'")

        if entry[-5] in [" ", "."]:
            raise ValueError("It is not possible to have space or dot before .txt in file name")

        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for character in entry[:-4]:
            if character in invalid_characters:
                raise ValueError(f"Any of the following are not allowed in a file name {invalid_characters}")
        return super(FileHandler, cls).__new__(cls)

    def __init__(self, file_name="log.txt"):

        self.file_name = file_name

    def __repr__(self):
        return f"FileHandler({self.file_name})"

    def __str__(self):
        return self.file_name

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

    def __repr__(self):
        return f"LogEntry({self.date}, {self.level}, {self.msg})"

    def __str__(self):
        return f"{self.date} | {self.level} | {self.msg}"

