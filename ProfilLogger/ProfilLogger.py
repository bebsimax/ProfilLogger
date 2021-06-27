import inspect
import datetime
import json


class ProfilLogger:
    """Class to save logs to the handlers

    Attributes:
        handlers (list): List of Handlers, viable Handlers are: FileHandler, CSVHandler, JsonHandler, SQLLiteHandler
        levels (dict): Dict of levels and it's values, the values are used to determine the order of levels
        log_level (str): One of levels keys, only logs with level equal or greater than levels[log_level] will be saved
    """

    def __new__(cls, handlers):
        """ProfilLogger constructor, implemented to avoid creation of Logger with wrong Type Handlers

        Args:
            handlers (list): List of Handlers, viable Handlers are: FileHandler, CSVHandler, JsonHandler, SQLLiteHandler
        """
        if not isinstance(handlers, list):
            raise TypeError("Passed argument must be a list")
        if len(handlers) == 0:
            raise TypeError("Passed list cannot be empty")
        viable_handlers = [FileHandler, CSVHandler, JsonHandler, SQLLiteHandler]
        for handler in handlers:
            for viable_handler in viable_handlers:
                if isinstance(handler, viable_handler):
                    break
            else:
                raise TypeError("Unsupported type passed as Handler")
        else:
            return super(ProfilLogger, cls).__new__(cls)

    def __init__(self, handlers):
        """ProfilLogger initializer

        Args:
            handlers (list): Initializes the handlers attribute
         """
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
        """repr used for developers"""
        return f"ProfiLogger(handlers={self.handlers})"

    def __str__(self):
        """str used for users"""
        return self.handlers

    def set_log_level(self, level):
        """Method used to change log_level of a ProfilLogger
        Args:
            level (str): level from a levels keys

        """
        if level in self.levels.keys():
            self.log_level = level

    def debug(self, msg):
        """Method used to create LogEntry with current date and message and debug level for every Handler,
        if the log_level is set below debug the LogEntry will not be created

        Args:
            msg (str): Message that will be saved in LogEntry
        """
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def info(self, msg):
        """Method used to create LogEntry with current date and message and info level for every Handler,
        if the log_level is set below info the LogEntry will not be created

        Args:
            msg (str): Message that will be saved in LogEntry
        """
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def warning(self, msg):
        """Method used to create LogEntry with current date and message and warning level for every Handler,
        if the log_level is set below warning the LogEntry will not be created

        Args:
            msg (str): Message that will be saved in LogEntry
        """
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def error(self, msg):
        """Method used to create LogEntry with current date and message and error level for every Handler,
        if the log_level is set below error the LogEntry will not be created

        Args:
            msg (str): Message that will be saved in LogEntry
        """
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))

    def critical(self, msg):
        """Method used to create LogEntry with current date and message and critical level for every Handler,
        if the log_level is set below critical the LogEntry will not be created

        Args:
            msg (str): Message that will be saved in LogEntry
        """
        method_name = inspect.currentframe().f_code.co_name
        if self.levels[method_name] >= self.levels[self.log_level]:
            for handler in self.handlers:
                handler.save(LogEntry(msg, method_name))


class FileHandler:
    """Class used to save and read LogEntry to and from .txt file

    Attributes:
        file_name (str): Name of a file to save to, or to read from. It works in current working directory.
    """

    def __new__(cls, entry="log.txt"):
        """FileHandler constructor creates instance only if entry is viable file name in all OS

        Args:
        entry (Optional[str]): name of a file to save to or read from, will default to log.txt if not specified
        """

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
        """FileHandler initializer

        Args:
            file_name (Optional[str]): Initializes the file_name attribute
        """
        self.file_name = file_name

    def __repr__(self):
        """repr used for developers"""
        return f"FileHandler({self.file_name})"

    def __str__(self):
        """str used for users"""
        return self.file_name

    def save(self, log_entry):
        """Saves LogEntry to a txt file specified in file_name
        separates date, level, msg with ;
        if LogEntry.msg contains ; it is replaced with :

        Args:
            log_entry (LogEntry): Instance of LogEntry class, containing date, level and msg
        """
        log_entry.msg.replace(";", ":")
        with open (self.file_name, "a", newline="\n") as file:
            file.write(f"{log_entry.date.strftime('%d %b %Y %H:%M:%S')} ; {log_entry.level} ; {log_entry.msg}\n")

    def read(self):
        """Yields LogEntry from file specified in file_name"""
        with open(self.file_name, "r", newline="\n") as file:
            whole_file = file.read()
            lines = whole_file.splitlines()
            lines = [line.split(";") for line in lines]
            for date, level, msg in tuple(lines):
                yield LogEntry(msg=msg.strip(), level=level.strip(), date=date.strip())


class CSVHandler:
    """Class used to save and read LogEntry to and from .csv file

    Attributes:
        file_name (str): Name of a file to save to, or to read from. It works in current working directory.
    """

    def __new__(cls, entry="log.csv"):
        """CSVHandler constructor creates instance only if entry is viable file name in all OS

            Args:
                entry (Optional[str]): name of a file to save to or read from, will default to log.csv if not specified
        """
        if entry == "log.csv":
            return super(CSVHandler, cls).__new__(cls)

        if not isinstance(entry, str):
            raise TypeError("Input should be a string")

        if len(entry) <= 4:
            raise ValueError("File name must be at least 5 characters long and include .csv at the end")

        if len(entry) >= 60:
            raise ValueError("Length of file name cannot get past 60 characters")

        if entry[-4:] != ".csv":
            raise ValueError("Passed file name does not end with '.csv'")

        if entry[-5] in [" ", "."]:
            raise ValueError("It is not possible to have space or dot before .csv in file name")

        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for character in entry[:-4]:
            if character in invalid_characters:
                raise ValueError(f"Any of the following are not allowed in a file name {invalid_characters}")
        return super(CSVHandler, cls).__new__(cls)

    def __init__(self, file_name="log.csv"):
        """CSVHandler initializer

            Args:
                file_name (Optional[str]): Initializes the file_name attribute
        """
        self.file_name = file_name

    def __repr__(self):
        """repr for developers"""
        return f"CSVHandler({self.file_name})"

    def __str__(self):
        """str for users"""
        return self.file_name

    def save(self, log_entry):
        """Saves LogEntry to a csv file specified in file_name

        Args:
            log_entry (LogEntry): Instance of LogEntry class, containing date, level and msg
        """
        import csv
        with open(self.file_name, "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([log_entry.date.strftime('%d %b %Y %H:%M:%S'), log_entry.level, log_entry.msg])

    def read(self):
        """Yields LogEntry from file specified in file_name"""
        import csv
        with open(self.file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                yield LogEntry(date=row[0], level=row[1], msg=row[2])


class JsonHandler:
    """Class used to save and read LogEntry to and from .json file

    Attributes:
        file_name (str): Name of a file to save to, or to read from. It works in current working directory.
    """

    def __new__(cls, entry="log.json"):
        """JsonHandler constructor creates instance only if entry is viable file name in all OS

            Args:
                entry (Optional[str]): name of a file to save to or read from, will default to log.json if not specified
        """
        if entry == "log.json":
            return super(JsonHandler, cls).__new__(cls)

        if not isinstance(entry, str):
            raise TypeError("Input should be a string")

        if len(entry) <= 5:
            raise ValueError("File name must be at least 6 characters long and include .json at the end")

        if len(entry) >= 60:
            raise ValueError("Length of file name cannot get past 60 characters")

        if entry[-5:] != ".json":
            raise ValueError("Passed file name does not end with '.json'")

        if entry[-6] in [" ", "."]:
            raise ValueError("It is not possible to have space or dot before .json in file name")

        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for character in entry[:-5]:
            if character in invalid_characters:
                raise ValueError(f"Any of the following are not allowed in a file name {invalid_characters}")
        return super(JsonHandler, cls).__new__(cls)

    def __init__(self, file_name="log.json"):
        """JsonHandler initializer

            Args:
                file_name (Optional[str]): Initializes the file_name attribute
        """
        self.file_name = file_name

    def __repr__(self):
        """repr for developers"""
        return f"JsonHandler({self.file_name})"

    def __str__(self):
        """str for users"""
        return self.file_name

    def save(self, log_entry):
        """Saves LogEntry to a json file specified in file_name

        Args:
            log_entry (LogEntry): Instance of LogEntry class, containing date, level and msg
        """

        class LogEncoder(json.JSONEncoder):
            def default(self, log):
                log.date = log.date.strftime('%d %b %Y %H:%M:%S')
                return log.__dict__

        with open(self.file_name, "a", newline='\n') as json_file:
            json.dump(log_entry, json_file, cls=LogEncoder)
            json_file.write('\n')

    def read(self):
        """Yields LogEntry from file specified in file_name"""
        with open(self.file_name, 'r') as json_file:
            for line in json_file:
                yield LogEntry(msg=json.loads(line)["msg"], level=json.loads(line)["level"], date=json.loads(line)["date"])


class SQLLiteHandler:
    """Class used to save and read LogEntry to and from .sqlite file

    Attributes:
        file_name (str): Name of a file to save to, or to read from. It works in current working directory.
    """

    def __new__(cls, entry="log.sqlite"):
        """SQLLiteHandler constructor creates instance only if entry is viable file name in all OS

            Args:
                entry (Optional[str]): name of a file to save to or read from, will default to log.sqlite if not specified
        """

        if entry == "log.sqlite":
            return super(SQLLiteHandler, cls).__new__(cls)

        if not isinstance(entry, str):
            raise TypeError("Input should be a string")

        if len(entry) <= 7:
            raise ValueError("File name must be at least 8 characters long and include .sqlite at the end")

        if len(entry) >= 60:
            raise ValueError("Length of file name cannot get past 60 characters")

        if entry[-7:] != ".sqlite":
            raise ValueError("Passed file name does not end with '.sqlite'")

        if entry[-8] in [" ", "."]:
            raise ValueError("It is not possible to have space or dot before .sqlite in file name")

        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for character in entry[:-7]:
            if character in invalid_characters:
                raise ValueError(f"Any of the following are not allowed in a file name {invalid_characters}")
        return super(SQLLiteHandler, cls).__new__(cls)

    def __init__(self, file_name="log.sqlite"):
        """SQLLiteHandler initializer

            Args:
                file_name (Optional[str]): Initializes the file_name attribute
        """
        self.file_name = file_name

    def save(self, log_entry):
        """Saves LogEntry to a sqlite file specified in file_name

        Args:
            log_entry (LogEntry): Instance of LogEntry class, containing date, level and msg
        """
        import sqlite3
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logs (date VARCHAR, level VARCHAR, msg VARCHAR);")
        cursor.execute(f"INSERT INTO logs (date, level, msg) VALUES "
                       f"('{log_entry.date.strftime('%d %b %Y %H:%M:%S')}',"
                       f"'{log_entry.level}',"
                       f"'{log_entry.msg}');")
        connection.commit()
        connection.close()

    def read(self):
        """Yields LogEntry from file specified in file_name"""
        import sqlite3
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        for row in cursor.execute("SELECT * FROM logs"):
            yield LogEntry(date=row[0], level=row[1], msg=row[2])
        connection.close()


class LogEntry:
    """Class used to represent logs

    Attributes:
        msg (str): Message of the log
        level (str): Level of the log
        date Optional([datetime]): Instance of datetime containing the date that the log was created,
        if not specified will default to current system's date
    """
    def __init__(self, msg, level, date=None):
        """LogEntry initializer

        Args:
            msg (str): Initializes the msg attribute
            level (str): Initializes the level attribute
            date Optional([str]): Initializes the date attribute, works only with date in "%d %b %Y %H:%M:%S" format
            if date is not specified will default to current system's date
        """
        if date:
            if isinstance(date, datetime.datetime):
                self.date = date
            else:
                try:
                    self.date = datetime.datetime.strptime(date, "%d %b %Y %H:%M:%S")
                except ValueError:
                    print("Wrong format of a date")
        else:
            self.date = datetime.datetime.now()
        self.level = level
        self.msg = msg

    def __repr__(self):
        """repr for developers"""
        return f"LogEntry({self.date}, {self.level}, {self.msg})"

    def __str__(self):
        """str for users"""
        return f"{self.date.strftime('%d %b %Y %H:%M:%S')} ; {self.level} ; {self.msg}"

    def __eq__(self, other):
        """method used during comparison of two LogEntry objects, returns True if both contain the same informations
        else returns False

        Args:
            other (LogEntry): Instance of LogEntry class, containing date, level and msg
        """
        if self.msg == other.msg:
            if self.level == other.level:
                if self.date == other.date:
                    return True
        return False


class ProfilLoggerReader:
    """Class used to receive filtered list of LogEntry instances

    Attributes:
        handler (Handler): Instance of a valid Handler
    """

    def __new__(cls, handler):
        """ProfilLoggerReader constructor prevents creation of LoggerReader with invalid Handler

        Args:
            handler (Handler): Instance of a valid Handler
        """
        viable_handlers = [FileHandler, CSVHandler, JsonHandler, SQLLiteHandler]
        for viable_handler in viable_handlers:
            if isinstance(handler, viable_handler):
                return super(ProfilLoggerReader, cls).__new__(cls)
        else:
            raise TypeError("Unsupported type passed as Handler")

    def __init__(self, handler):
        """ProfilLoggerReader initializer

        Args:
            handler (Handler): Initializes the handler value
        """
        self.handler = handler

    def find_by_text(self, text, start_date=None, end_date=None):
        """Method used to get filter list of LogEntry instances from file specified in handler's file_name
        Needs to filter by text, can also filter by dates

        Args:
            text (str): Text that LogEntry.msg must contain
            start_date Optional([str]): Date in iso format. If passed will filter logs with date past the start_date
            end_date Optional([str]): Date in iso format. If passed will filter logs with date before the end_date.:
        """
        if not isinstance(text, str):
            raise TypeError("Text needs to be a string")

        # start_date validation
        if start_date:
            if isinstance(start_date, datetime.datetime):
                pass
            else:
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.datetime.fromisoformat(start_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")

        # end_date validation
        if end_date:
            if isinstance(end_date, datetime.datetime):
                pass
            else:
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.datetime.fromisoformat(end_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be past start_date")

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
        """Method used to get filter list of LogEntry instances from file specified in handler's file_name
            Needs to filter by regular expression, can also filter by dates

            Args:
                regex (str): Valid regular expression, will be searched for in LogEntry.msg
                start_date Optional([str]): Date in iso format. If passed will filter logs with date past the start_date
                end_date Optional([str]): Date in iso format. If passed will filter logs with date before the end_date
        """
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
            if isinstance(start_date, datetime.datetime):
                pass
            else:
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.datetime.fromisoformat(start_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")

        # end_date validation
        if end_date:
            if isinstance(end_date, datetime.datetime):
                pass
            else:
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.datetime.fromisoformat(end_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be past start_date")

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
        """Method used to get grouped by level dict of LogEntry instances from file specified in handler's file_name
            Can filter by dates

            Args:
                start_date Optional([str]): Date in iso format. If passed will filter logs with date past the start_date
                end_date Optional([str]): Date in iso format. If passed will filter logs with date before the end_date
        """
        # start_date validation
        if start_date:
            if isinstance(start_date, datetime.datetime):
                pass
            else:
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.datetime.fromisoformat(start_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")

        # end_date validation
        if end_date:
            if isinstance(end_date, datetime.datetime):
                pass
            else:
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.datetime.fromisoformat(end_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be past start_date")
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

    def groupby_month(self, start_date=None, end_date=None):
        """Method used to get grouped by month dict of LogEntry instances from file specified in handler's file_name
            Can filter by dates

            Args:
                start_date Optional([str]): Date in iso format. If passed will filter logs with date past the start_date
                end_date Optional([str]): Date in iso format. If passed will filter logs with date before the end_date
        """
        # start_date validation
        if start_date:
            if isinstance(start_date, datetime.datetime):
                pass
            else:
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.datetime.fromisoformat(start_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")

        # end_date validation
        if end_date:
            if isinstance(end_date, datetime.datetime):
                pass
            else:
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.datetime.fromisoformat(end_date)
                    except ValueError:
                        raise ValueError("Please use iso format")
                else:
                    raise TypeError("start_date needs to be a string")
            if start_date:
                if end_date < start_date:
                    raise ValueError("end_date needs to be past start_date")
        log_dict = {}
        if not start_date and not end_date:
            for log in self.handler.read():
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)

        if start_date and not end_date:
            for log in self.handler.read():
                if start_date <= log.date:
                    if log.date.month not in log_dict.keys():
                        log_dict[log.date.month] = []
                    log_dict[log.date.month].append(log)

        if not start_date and end_date:
            for log in self.handler.read():
                if log.date <= end_date:
                    if log.date.month not in log_dict.keys():
                        log_dict[log.date.month] = []
                    log_dict[log.date.month].append(log)

        if start_date and end_date:
            for log in self.handler.read():
                if start_date <= log.date <= end_date:
                    if log.date.month not in log_dict.keys():
                        log_dict[log.date.month] = []
                    log_dict[log.date.month].append(log)

        return log_dict
