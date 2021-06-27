import unittest
import os
import sys

# Jan is a careful developer who prefers logging over print statements
# He has heard about new custom logger called ProfilLogger
# He quickly imports it inside his working file


os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
logger_path = (os.path.join(os.path.dirname(CUR_DIR), 'ProfilLogger'))
sys.path.append(logger_path)

from ProfilLogger.ProfilLogger import ProfilLogger, FileHandler, CSVHandler, JsonHandler, SQLLiteHandler, LogEntry, ProfilLoggerReader


class UsageTest(unittest.TestCase):

    def setUp(self):
        global my_logger
        my_logger = ProfilLogger(handlers=[FileHandler()])

    def tearDown(self):
        try:
            os.remove('log.txt')
        except OSError:
            pass
        try:
            os.remove('log.csv')
        except OSError:
            pass
        try:
            os.remove('log.json')
        except OSError:
            pass
        try:
            os.remove('log.sqlite')
        except OSError:
            pass

    def test_logger_not_always_creates_a_file(self):
        # Before logging his current work he decides to test the new logger
        # But, he has no idea how it works
        # He checks the docstring
        # help(ProfilLogger)
        # It contains information about the class and it's methods
        # Happy with the outcome Jan starts to read
        # He finds about the info method
        # Jan decides to try it on his new object
        my_logger.info("My first info message")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        # The operation didn't cause error, and he didn't notice any new file in his working directory
        self.assertTrue("log.txt" not in files,
                        "Info method created empty log.txt file")

    def test_warning_is_default_log_level(self):
        # He reads the help once again, only to find about the default setting for log entry is warning
        self.assertEqual(my_logger.log_level, "warning",
                         "warning is not the default log level")

    def test_logger_saves_logs_only_when_needed(self):
        # He changes it to INFO using method set_log_level
        my_logger.set_log_level("info")

        # He tries saving INFO log once again
        my_logger.info("My first info message")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        # This time the file log.txt is created
        self.assertIn("log.txt", files,
                      "Info method didn't create log.log file")

        # His new shiny file contains his, message
        with open ("log.txt", "r") as file:
            whole_text = file.read()
            lines = whole_text.splitlines()
            self.assertTrue("My first info message" in lines[0],
                            "info didn't save message to file")

        # Jan adds warning level message to his log
        my_logger.warning("My first warning message")

        # He checks if it created a new entry in his log.txt file
        with open("log.txt", "r") as file:
            whole_text = file.read()
            lines = whole_text.splitlines()
            self.assertTrue("My first warning message" in lines[1],
                            "warning didn't save message to file")

    def test_ProfilLoggerReader_returns_LogEntries(self):
        # Jan is satisfied with loggers work so far, but manually checking files made him dizzy
        # So he creates instance of FileHandler
        my_file_handler = FileHandler("log.txt")
        # He passes it as an argument to the ProlifLogger, and quickly creates some logs
        my_logger = ProfilLogger(handlers=[my_file_handler])
        my_logger.set_log_level("debug")
        my_logger.debug("This is debug message")
        my_logger.info("This is info message")
        my_logger.warning("This is warning message")
        my_logger.error("This is error message")
        my_logger.critical("This is critical message")
        # Now he creates his ProfilLoggerReader instance
        my_file_reader = ProfilLoggerReader(handler=my_file_handler)
        # After that, he checks if method "find_by_text" returns his logs as a list of LogsEntries
        log_list = my_file_reader.find_by_text("message")
        for log in log_list:
            self.assertTrue(isinstance(log, LogEntry))
        # Next, he checks if method "find_by_regex" returns his logs as a list of LogsEntries
        regex_log_list = my_file_reader.find_by_regex("[a-g] message")
        for log in regex_log_list:
            self.assertTrue(isinstance(log, LogEntry))

    def test_ProfilLoggerReader_returns_list_of_LogEntry_for_every_handler(self):
        # Jan decides to test all supported file types
        my_file_handler = FileHandler()
        my_csv_handler = CSVHandler()
        my_json_handler = JsonHandler()
        my_sqlite_handler = SQLLiteHandler()
        # He creates logger with all handlers
        my_logger = ProfilLogger(handlers=[my_file_handler, my_csv_handler, my_json_handler, my_sqlite_handler])
        # Writes down some logs
        my_logger.set_log_level("info")
        my_logger.info("info message")
        my_logger.warning("warning message")
        my_logger.error("error message")
        my_logger.critical("critical message")
        # And creates reader for each type
        my_file_reader = ProfilLoggerReader(handler=my_file_handler)
        my_csv_reader = ProfilLoggerReader(handler=my_csv_handler)
        my_json_reader = ProfilLoggerReader(handler=my_json_handler)
        my_sqlite_reader = ProfilLoggerReader(handler=my_sqlite_handler)
        # Reads logs with given message to separate lists
        logs_from_file = my_file_reader.find_by_text("message")
        logs_from_csv = my_csv_reader.find_by_text("message")
        logs_from_json = my_json_reader.find_by_text("message")
        logs_from_sqlite = my_sqlite_reader.find_by_text("message")
        # And checks if all messages were saved, and if objects are instances of LogEntry
        all_logs = [logs_from_file, logs_from_csv, logs_from_json, logs_from_sqlite]
        for log_list in all_logs:
            self.assertEqual(len(log_list), 4,
                             "Didn't save all")
            for log in log_list:
                self.assertTrue(isinstance(log,  LogEntry),
                                "It's not a log")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
