import os
import inspect
import datetime


class ProfilLogger:
    """Stop it, get some help"""

    def __new__(cls, handlers):
        viable_handlers = [FileHandler]
        for handler in handlers:
            for viable_handler in viable_handlers:
                if isinstance(handler, viable_handler):
                    break
            else:
                raise TypeError("Unsupported type passed as Handler")
        else:
            return super(ProfilLogger, cls).__new__(cls)

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
            file.write(f"{log_entry.date.strftime('%d %b %Y %H:%M:%S')} ; {log_entry.level} ; {log_entry.msg}\n")

    def read(self):
        with open(self.file_name, "r", newline="\n") as file:
            whole_file = file.read()
            lines = whole_file.splitlines()
            lines = [line.split(";") for line in lines]
            for date, level, msg in tuple(lines):
                yield LogEntry(msg=msg.strip(), level=level.strip(), date=date.strip())


class LogEntry:
    """Creates log entries"""
    def __init__(self, msg, level, date=None):
        self.msg = msg
        self.level = level
        if date:
            try:
                self.date = datetime.datetime.strptime(date, "%d %b %Y %H:%M:%S")
            except ValueError:
                print("Wrong format of a date")
        else:
            self.date = datetime.datetime.now()

    def __repr__(self):
        return f"LogEntry({self.date}, {self.level}, {self.msg})"

    def __str__(self):
        return f"{self.date.strftime('%d %b %Y %H:%M:%S')} ; {self.level} ; {self.msg}"

    def __eq__(self, other):
        if self.msg == other.msg:
            if self.level == other.level:
                if self.date == other.date:
                    return True
        return False


class ProfilLoggerReader:

    def __new__(cls, handler):
        viable_handlers = [FileHandler]
        for viable_handler in viable_handlers:
            if isinstance(handler, viable_handler):
                return super(ProfilLoggerReader, cls).__new__(cls)
        else:
            raise TypeError("Unsupported type passed as Handler")

    def __init__(self, handler):
        self.handler = handler

    def find_by_text(self, text, start_date=None, end_date=None):
        if not isinstance(text, str):
            raise TypeError("Text needs to be a string")

        # start_date validation
        if start_date:
            if not isinstance(start_date, str):
                raise TypeError("start_date needs to be a string")
            try:
                start_date = datetime.datetime.fromisoformat(start_date)
            except ValueError:
                raise ValueError("Please use iso format")
        # end_date validation
        if end_date:
            if not isinstance(end_date, str):
                raise TypeError("end_date needs to be a string")
            try:
                end_date = datetime.datetime.fromisoformat(end_date)
            except ValueError:
                raise ValueError("Please use iso format")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be later than start_date")

        # filtration of logs based on passed arguments
        if not start_date and not end_date:
            filtered_logs = [log for log in self.handler.read() if text in log.msg]
        if start_date and not end_date:
            filtered_logs = [log for log in self.handler.read() if text in log.msg and start_date <= log.date]
        if not start_date and end_date:
            filtered_logs = [log for log in self.handler.read() if text in log.msg and log.date <= end_date]
        if start_date and end_date:
            filtered_logs = [log for log in self.handler.read() if text in log.msg and start_date <= log.date <= end_date]

        return filtered_logs

    def find_by_regex(self, regex, start_date=None, end_date=None):
        import re
        # regex validation
        if not isinstance(regex, str):
            raise TypeError("Regex needs to be a string")
        try:
            re.compile(regex)
        except re.error as error:
            raise re.error(error)

        # start_date validation
        if start_date:
            if not isinstance(start_date, str):
                raise TypeError("start_date needs to be a string")
            try:
                start_date = datetime.datetime.fromisoformat(start_date)
            except ValueError:
                raise ValueError("Please use iso format")
        # end_date validation
        if end_date:
            if not isinstance(end_date, str):
                raise TypeError("end_date needs to be a string")
            try:
                end_date = datetime.datetime.fromisoformat(end_date)
            except ValueError:
                raise ValueError("Please use iso format")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be later than start_date")

        # filtration of logs based on passed arguments
        if not start_date and not end_date:
            filtered_logs = [log for log in self.handler.read() if re.search(regex, log.msg)]
        if start_date and not end_date:
            filtered_logs = [log for log in self.handler.read() if re.search(regex, log.msg)
                                                                and start_date <= log.date]
        if not start_date and end_date:
            filtered_logs = [log for log in self.handler.read() if re.search(regex, log.msg)
                                                                and log.date <= end_date]
        if start_date and end_date:
            filtered_logs = [log for log in self.handler.read() if
                             re.search(regex, log.msg) and start_date <= log.date <= end_date]
        return filtered_logs

    def groupby_level(self, start_date=None, end_date=None):
        # start_date validation
        if start_date:
            if not isinstance(start_date, str):
                raise TypeError("start_date needs to be a string")
            try:
                start_date = datetime.datetime.fromisoformat(start_date)
            except ValueError:
                raise ValueError("Please use iso format")
        # end_date validation
        if end_date:
            if not isinstance(end_date, str):
                raise TypeError("end_date needs to be a string")
            try:
                end_date = datetime.datetime.fromisoformat(end_date)
            except ValueError:
                raise ValueError("Please use iso format")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be later than start_date")
        log_dict = {}
        if not start_date and not end_date:
            for log in self.handler.read():
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)

        if start_date and not end_date:
            for log in self.handler.read():
                if start_date <= log.date:
                    if log.level not in log_dict.keys():
                        log_dict[log.level] = []
                    log_dict[log.level].append(log)

        if not start_date and end_date:
            for log in self.handler.read():
                if log.date <= end_date:
                    if log.level not in log_dict.keys():
                        log_dict[log.level] = []
                    log_dict[log.level].append(log)

        if start_date and end_date:
            for log in self.handler.read():
                if start_date <= log.date <= end_date:
                    if log.level not in log_dict.keys():
                        log_dict[log.level] = []
                    log_dict[log.level].append(log)

        return log_dict
