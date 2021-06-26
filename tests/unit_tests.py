import unittest
import os
import sys
import random
import datetime
import re
import csv
import json
os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
src_path = (os.path.join(os.path.dirname(CUR_DIR), 'src'))
zad_rek_path = os.path.join(src_path, 'zad_rek')
sys.path.append(zad_rek_path)

from ProfilLogger import ProfilLogger, FileHandler, LogEntry, ProfilLoggerReader, CSVHandler, JsonHandler


class ProfilLoggerTest(unittest.TestCase):

    def test_logger_has_default_warning_level(self):
        logger = ProfilLogger(handlers=[FileHandler()])
        self.assertEqual(logger.log_level, "warning",
                         "warning is not default log level")

    def test_set_log_level_method_changes_log_level(self):
        logger = ProfilLogger(handlers=[FileHandler()])
        logger.set_log_level("info")
        self.assertEqual(logger.log_level, "info",
                         "set_log_method didn't change log level")

    def test_set_log_level_method_does_not_change_level_when_input_is_not_known(self):
        logger = ProfilLogger(handlers=[FileHandler()])
        logger.set_log_level("WE DO IT LIVE")
        self.assertEqual(logger.log_level, "warning",
                         "set_log_method changed log level after receiving invalid input")

    def test_logger_raises_TypeError_when_passed_wrong_type_as_Handler(self):
        with self.assertRaises(TypeError):
            ProfilLogger(handlers=[11])
            ProfilLogger(handlers=["log.txt"])


class ProfilLoggerFileHandlerTest(unittest.TestCase):

    def setUp(self):
        global logger
        logger = ProfilLogger(handlers=[FileHandler()])

    def tearDown(self):
        try:
            os.remove('log.txt')
        except OSError:
            pass

    def test_logger_can_save_message_to_file(self):
        logger.warning("This is your last warning")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertIn("log.txt", files,
                      "Warning method didn't create log.txt file")
        with open("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            self.assertTrue("This is your last warning" in lines[0],
                            "warning didn't save message")

    def test_logger_saves_all_log_levels_that_he_needs_to_save(self):
        levels = list(logger.levels.keys())
        selected_level = random.choice(levels)
        logger.set_log_level(selected_level)
        levels_to_write = [name for name in levels if logger.levels[selected_level] <= logger.levels[name]]
        for method in levels:
            class_method = getattr(logger, method)
            class_method(f"This is test message for {method}")
        with open("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            for method in levels_to_write:
                for line in lines:
                    if f"This is test message for {method}" in line:
                        break
                else:
                    self.fail(f"{method} didn't create a sample text")

    def test_logger_does_not_save_logs_that_do_not_need_to_be_saved(self):
        levels = list(logger.levels.keys())
        selected_level = random.choice(levels)
        logger.set_log_level(selected_level)
        levels_to_write = [name for name in levels if logger.levels[selected_level] <= logger.levels[name]]
        for method in levels:
            class_method = getattr(logger, method)
            class_method(f"This is test message for {method}")
        with open("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            levels_not_to_write = set(levels) - set(levels_to_write)
            for method in levels_not_to_write:
                for line in lines:
                    if f"This is test message for {method}" in line:
                        self.fail(f"{method} created log when it shouldn't")

    def test_logger_can_save_to_two_txt_files_at_once(self):
        import datetime
        first_handler = FileHandler("first.txt")
        second_handler = FileHandler("second.txt")
        my_logger = ProfilLogger(handlers=[first_handler, second_handler])
        now = datetime.datetime.now()
        my_logger.warning("Are you still there?")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        with open ("first.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            line_in_first = lines[0]
            self.assertEqual(line_in_first, (f"{formatted_now} ; warning ; Are you still there?"),
                             "Warning didn't save message to the first.txt file")
        with open ("second.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            line_in_second = lines[0]
            self.assertEqual(line_in_second, (f"{formatted_now} ; warning ; Are you still there?"),
                             "Warning didn't save message to the second.txt file")

        self.assertEqual(line_in_first, line_in_second,
                         "Saved lines aren't equal")

        try:
            os.remove('first.txt')
        except OSError:
            pass
        try:
            os.remove('second.txt')
        except OSError:
            pass


class ProfilLoggerCSVHandlerTest(unittest.TestCase):

    def setUp(self):
        global logger
        logger = ProfilLogger(handlers=[CSVHandler()])

    def tearDown(self):
        try:
            os.remove('log.csv')
        except OSError as error:
            pass

    def test_logger_can_save_message_to_csv_file(self):
        logger.warning("This is your last warning")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertIn("log.csv", files,
                      "Warning method didn't create log.csv file")
        with open("log.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.assertTrue("This is your last warning" in row[2],
                                "didn't save message to csv file")

    def test_logger_saves_all_log_levels_that_he_needs_to_save(self):
        levels = list(logger.levels.keys())
        selected_level = random.choice(levels)
        logger.set_log_level(selected_level)
        levels_to_write = [name for name in levels if logger.levels[selected_level] <= logger.levels[name]]
        for method in levels:
            class_method = getattr(logger, method)
            class_method(f"This is test message for {method}")
        with open("log.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for method in levels_to_write:
                for row in csv_reader:
                    if f"This is test message for {method}" in row[2]:
                        break
                else:
                    self.fail(f"{method} didn't create a sample text")

    def test_logger_does_not_save_logs_that_do_not_need_to_be_saved(self):
        levels = list(logger.levels.keys())
        selected_level = random.choice(levels)
        logger.set_log_level(selected_level)
        levels_to_write = [name for name in levels if logger.levels[selected_level] <= logger.levels[name]]
        for method in levels:
            class_method = getattr(logger, method)
            class_method(f"This is test message for {method}")
        with open("log.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            levels_not_to_write = set(levels) - set(levels_to_write)
            for method in levels_not_to_write:
                for row in csv_reader:
                    if f"This is test message for {method}" in row[2]:
                        self.fail(f"{method} created log when it shouldn't")

    def test_logger_can_save_to_two_csv_files_at_once(self):
        import datetime
        first_handler = CSVHandler("first.csv")
        second_handler = CSVHandler("second.csv")
        my_logger = ProfilLogger(handlers=[first_handler, second_handler])
        now = datetime.datetime.now()
        my_logger.warning("Are you still there?")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        with open("first.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                line_in_first = row
                self.assertEqual(f"{row[0]},{row[1]},{row[2]}", f"{formatted_now},warning,Are you still there?",
                            "Warning didn't save message to the first.csv file")
        with open("second.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                line_in_second = row
                self.assertEqual(f"{row[0]},{row[1]},{row[2]}", f"{formatted_now},warning,Are you still there?",
                                 "Warning didn't save message to the second.csv file")

                self.assertEqual(line_in_first, line_in_second,
                                "Saved lines aren't equal")
        try:
            os.remove('first.csv')
        except OSError:
            pass
        try:
            os.remove('second.csv')
        except OSError:
            pass


class FileHandlerTest(unittest.TestCase):

    def setUp(self):
        global file_handler
        file_handler = FileHandler()

    def tearDown(self):
        try:
            os.remove('log.txt')
        except OSError as error:
            #print(error)
            #print("log.txt NOT REMOVED")
            pass
        try:
            os.remove('sample.txt')
        except OSError as error:
            #print(error)
            #print("sample.txt NOT REMOVED")
            pass

    def test_file_handler_default_file_name_is_log_txt(self):
        self.assertEqual(file_handler.file_name, "log.txt",
                         "log.txt is not default file name")

    def test_file_handler_saves_file_name_given_during_creation(self):
        file_handler = FileHandler("logger.txt")
        self.assertEqual(file_handler.file_name, "logger.txt",
                         "FileHandler didn't change file_name during creation")

    def test_file_handler_creates_log_txt_by_default(self):
        now = datetime.datetime.now()
        my_log = LogEntry("this is message", "this is level")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        file_handler.save(my_log)
        with open ("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            lines = [component.strip() for component in lines[0].split(";")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formatted_now,
                         "FileHandler didn't save date")
        self.assertEqual(msg, "this is message",
                         "FileHandler didn't save msg")
        self.assertEqual(level, "this is level",
                         "FileHandler didn't save level")

    def test_file_handler_creates_log_with_specified_name(self):
        now = datetime.datetime.now()
        my_log = LogEntry("this is message", "this is level")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        file_handler = FileHandler("sample.txt")
        file_handler.save(my_log)
        with open("sample.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            lines = [component.strip() for component in lines[0].split(";")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formatted_now,
                         "FileHandler didn't save date")
        self.assertEqual(msg, "this is message",
                         "FileHandler didn't save msg")
        self.assertEqual(level, "this is level",
                         "FileHandler didn't save level")

    def test_file_handler_returns_TypeError_when_passed_wrong_type(self):
        with self.assertRaises(TypeError):
            FileHandler(11)

    def test_file_handler_returns_ValueError_when_input_is_too_short(self):
        with self.assertRaises(ValueError):
            FileHandler("log")

    def test_file_handler_returns_ValueError_when_input_is_too_long(self):
        with self.assertRaises(ValueError):
            FileHandler("logloglogloglogloglogloglogloglogloglogloglogloglogloglogloglogloglog.txt")

    def test_file_handler_returns_ValueError_when_input_does_not_end_with_dottxt(self):
        with self.assertRaises(ValueError):
            FileHandler("logloglog.json")

    def test_file_handler_returns_ValueError_when_file_name_ends_with_space(self):
        with self.assertRaises(ValueError):
            FileHandler("logloglog .txt")

    def test_file_handler_returns_ValueError_when_file_name_ends_with_dot(self):
        with self.assertRaises(ValueError):
            FileHandler("logloglog..txt")

    def test_file_handler_returns_ValueError_when_file_contains_invalid_character(self):
        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for invalid in invalid_characters:
            with self.assertRaises(ValueError):
                FileHandler(f"loglogl{invalid}g.txt")

    def test_read_method_returns_all_logs_in_form_of_LogEntries(self):
        my_handler = FileHandler("test_log.txt")
        my_logger = ProfilLogger(handlers=[my_handler])
        my_logger.set_log_level("debug")
        my_logger.debug("This is debug message")
        my_logger.info("This is info message")
        my_logger.warning("This is warning message")
        my_logger.error("This is error message")
        my_logger.critical("This is critical message")
        list_of_logs = my_handler.read()
        try:
            for log in list_of_logs:
                self.assertTrue(isinstance(log, LogEntry),
                                f"{log} is not an instance of LogEntry")

        except TypeError:
            pass
        finally:
            try:
                os.remove('test_log.txt')
            except OSError as error:
                print(error)


class CSVHandlerTest(unittest.TestCase):

    def setUp(self):
        global csv_handler
        csv_handler = CSVHandler()

    def tearDown(self):
        try:
            os.remove('log.csv')
        except OSError:
            pass
        try:
            os.remove('sample.csv')
        except OSError:
            pass

    def test_csv_handler_default_file_name_is_log_csv(self):
        self.assertEqual(csv_handler.file_name, "log.csv",
                         "log.csv is not default file name")

    def test_csv_handler_saves_file_name_given_during_creation(self):
        csv_handler = CSVHandler("logger.csv")
        self.assertEqual(csv_handler.file_name, "logger.csv",
                         "CSVHandler didn't change file_name during creation")

    def test_csv_handler_creates_log_csv_by_default(self):
        now = datetime.datetime.now()
        my_log = LogEntry("i'm in danger", "danger")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        csv_handler.save(my_log)
        with open("log.csv", "r", newline="\n") as csv_file:
            file_content = csv_file.read()
            lines = file_content.splitlines()
            lines = [component for component in lines[0].split(",")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formatted_now,
                         "CSVHandler didn't save date")
        self.assertEqual(msg, "i'm in danger",
                         "CSVHandler didn't save msg")
        self.assertEqual(level, "danger",
                         "CSVHandler didn't save level")

    def test_csv_handler_creates_log_with_specified_name(self):
        now = datetime.datetime.now()
        my_log = LogEntry("info is informative", "info")
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        csv_handler = CSVHandler("sample.csv")
        csv_handler.save(my_log)
        with open("sample.csv", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            lines = [component.strip() for component in lines[0].split(",")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formatted_now,
                         "CSVHandler didn't save date")
        self.assertEqual(msg, "info is informative",
                         "CSVHandler didn't save msg")
        self.assertEqual(level, "info",
                         "CSVHandler didn't save level")

    def test_csv_handler_returns_TypeError_when_passed_wrong_type(self):
        with self.assertRaises(TypeError):
            CSVHandler(11)

    def test_csv_handler_returns_ValueError_when_input_is_too_short(self):
        with self.assertRaises(ValueError):
            CSVHandler("log")

    def test_csv_handler_returns_ValueError_when_input_is_too_long(self):
        with self.assertRaises(ValueError):
            CSVHandler("logloglogloglogloglogloglogloglogloglogloglogloglogloglogloglogloglog.csv")

    def test_csv_handler_returns_ValueError_when_input_does_not_end_with_dottxt(self):
        with self.assertRaises(ValueError):
            CSVHandler("logloglog.json")

    def test_csv_handler_returns_ValueError_when_file_name_ends_with_space(self):
        with self.assertRaises(ValueError):
            CSVHandler("logloglog .csv")

    def test_csv_handler_returns_ValueError_when_file_name_ends_with_dot(self):
        with self.assertRaises(ValueError):
            CSVHandler("logloglog..csv")

    def test_csv_handler_returns_ValueError_when_file_contains_invalid_character(self):
        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for invalid in invalid_characters:
            with self.assertRaises(ValueError):
                CSVHandler(f"loglogl{invalid}g.csv")

    def test_read_method_returns_all_logs_in_form_of_LogEntries(self):
        my_handler = CSVHandler("log.csv")
        my_logger = ProfilLogger(handlers=[my_handler])
        my_logger.set_log_level("debug")
        my_logger.debug("This is debug message")
        my_logger.info("This is info message")
        my_logger.warning("This is warning message")
        my_logger.error("This is error message")
        my_logger.critical("This is critical message")
        for log in my_handler.read():
            self.assertTrue(isinstance(log, LogEntry),
                            f"{log} is not an instance of LogEntry")


class JsonHandlerTest(unittest.TestCase):

    def setUp(self):
        global json_handler
        json_handler = JsonHandler()

    def tearDown(self):
        try:
            os.remove('log.json')
        except OSError:
            pass
        try:
            os.remove('sample.json')
        except OSError:
            pass

    def test_json_handler_default_file_name_is_log_json(self):
        self.assertEqual(json_handler.file_name, "log.json",
                         "log.json is not default file name")

    def test_json_handler_saves_file_name_given_during_creation(self):
        json_handler = JsonHandler("logger.json")
        self.assertEqual(json_handler.file_name, "logger.json",
                         "CSVHandler didn't change file_name during creation")

    def test_json_handler_creates_log_json_by_default(self):
        my_log = LogEntry("morning", "debug")
        json_handler.save(my_log)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertTrue("log.json" in files)

    def test_json_handler_creates_log_with_specified_name(self):
        my_log = LogEntry(msg="Message", level="warning")
        my_json_handler = JsonHandler("sample.json")
        my_json_handler.save(my_log)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertTrue("sample.json" in files)

    def test_json_handler_returns_TypeError_when_passed_wrong_type(self):
        with self.assertRaises(TypeError):
            JsonHandler(11)

    def test_json_handler_returns_ValueError_when_input_is_too_short(self):
        with self.assertRaises(ValueError):
            JsonHandler("log")

    def test_json_handler_returns_ValueError_when_input_is_too_long(self):
        with self.assertRaises(ValueError):
            JsonHandler("logloglogloglogloglogloglogloglogloglogloglogloglogloglogloglogloglog.json")

    def test_json_handler_returns_ValueError_when_input_does_not_end_with_dotjson(self):
        with self.assertRaises(ValueError):
            JsonHandler("logloglog.txt")

    def test_json_handler_returns_ValueError_when_file_name_ends_with_space(self):
        with self.assertRaises(ValueError):
            JsonHandler("logloglog .json")

    def test_json_handler_returns_ValueError_when_file_name_ends_with_dot(self):
        with self.assertRaises(ValueError):
            JsonHandler("logloglog..json")

    def test_json_handler_returns_ValueError_when_file_contains_invalid_character(self):
        invalid_characters = ["\\", "/", ":", "*", '"', "<", ">", "|"]
        for invalid in invalid_characters:
            with self.assertRaises(ValueError):
                JsonHandler(f"loglogl{invalid}g.json")

    def test_read_method_returns_all_logs_in_form_of_LogEntries(self):
        my_handler = JsonHandler("log.json")
        my_logger = ProfilLogger(handlers=[my_handler])
        my_logger.set_log_level("debug")
        my_logger.debug("This is debug message")
        my_logger.info("This is info message")
        my_logger.warning("This is warning message")
        my_logger.error("This is error message")
        my_logger.critical("This is critical message")
        for log in my_handler.read():
            self.assertTrue(isinstance(log, LogEntry),
                            f"{log} is not an instance of LogEntry")


class LogEntryTest(unittest.TestCase):

    def test_LogEntry_stores_user_message(self):
        message = "I am logging"
        level = "info"
        entry = LogEntry(message, level)
        self.assertEqual(message, entry.msg,
                         "LogEntry didn't store message")

    def test_LogEntry_stores_level(self):
        message = "Boxes"
        level = "info"
        entry = LogEntry(message, level)
        self.assertEqual(entry.level, level,
                         "LogEntry didn't store level")

    def test_LogEntry_stores_datetime(self):
        message = "I am logging"
        level = "debug"
        entry = LogEntry(message, level)
        date_from_log = entry.date
        self.assertTrue(date_from_log, datetime.datetime)

    def test_printed_LogEntry_returns_correct_text(self):
        msg = "The message"
        level = "info"
        now = datetime.datetime.now()
        entry = LogEntry(msg, level=level)
        formatted_now = now.strftime("%d %b %Y %H:%M:%S")
        self.assertEqual(entry.__str__(), f"{formatted_now} ; {level} ; {msg}",
                         "LogEntry does not print the way it should")

    def test_LogEntries_date_can_be_compared_to_other_dates(self):
        now = datetime.datetime.now()
        log = LogEntry(msg="Msg", level="info")
        self.assertTrue(log.date <= now)


class ProfilLoggerReaderTest(unittest.TestCase):

    def test_logger_reader_cannot_be_created_without_passing_an_argument(self):
        with self.assertRaises(TypeError):
            ProfilLoggerReader()

    def test_logger_reader_cannot_be_created_without_valid_handler(self):
        with self.assertRaises(TypeError):
            ProfilLoggerReader(handler="log.txt")

    def test_logger_reader_rises_TypeError_when_receiving_more_than_one_handler(self):
        first = FileHandler("first.txt")
        second = CSVHandler("second.csv")
        with self.assertRaises(TypeError):
            ProfilLoggerReader(handler=[first, second])

    def test_logger_reader_can_be_created_with_correct_handler(self):
        my_handler = FileHandler("logs.txt")
        my_logger_reader = ProfilLoggerReader(my_handler)
        self.assertTrue(isinstance(my_logger_reader, ProfilLoggerReader))


class ProfilLoggerReaderFileHandlerTest(unittest.TestCase):

    def setUp(self):
        global my_file_handler
        my_file_handler = FileHandler("FileHandler_sample_data.txt")

    def test_reader_saves_file_handler_in_his_instance(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        self.assertTrue(my_reader.handler is my_file_handler)

    def test_find_by_text_returns_empty_list_when_text_does_not_match_any_EntryLog_msg(self):
        text = "I like cup of tea in the morning"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text)
        self.assertEqual(logs_returned, [],
                         "Reader didn't return empty list")

    def test_find_by_text_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.find_by_text(text="hopsa lala", start_date=start_date, end_date=end_date)

    def test_find_by_text_works_with_only_text_input(self):
        text = "debug"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text)
        logs_filtered = [log for log in my_file_handler.read() if text in log.msg]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_and_start_date_input(self):
        text = "info"
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text, start_date=start_date)
        logs_filtered = [log for log in my_file_handler.read() if text in log.msg
                         and start_date_as_datetime <= log.date]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_and_end_date_input(self):
        text = "warning"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text, end_date=end_date)
        logs_filtered = [log for log in my_file_handler.read() if text in log.msg
                         and log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_start_and_end_dates_input(self):
        text = "error"
        start_date = "2021-06-22"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text, start_date=start_date, end_date=end_date)
        logs_filtered = [log for log in my_file_handler.read() if text in log.msg
                         and start_date_as_datetime <= log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_returns_empty_list_when_text_does_not_match_any_EntryLog_msg(self):
        regex = r"\d"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex)
        self.assertEqual(logs_returned, [],
                         "Reader didn't return empty list")

    def test_find_by_regex_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.find_by_regex(regex="\d", start_date=start_date, end_date=end_date)

    def test_find_by_regex_works_with_only_regex_input(self):
        regex = r"[a-g] message"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex)
        logs_filtered = [log for log in my_file_handler.read() if re.search(regex, log.msg)]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_and_start_date_input(self):
        regex = r"[l-m] message"
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, start_date=start_date)
        logs_filtered = [log for log in my_file_handler.read() if re.search(regex, log.msg)
                         and start_date_as_datetime <= log.date]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_and_end_date_input(self):
        regex = r"[n-p] message"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, end_date=end_date)
        logs_filtered = [log for log in my_file_handler.read() if re.search(regex, log.msg)
                         and log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_start_and_end_dates_input(self):
        regex = r"[r-z] message"
        start_date = "2021-06-22"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, start_date=start_date, end_date=end_date)
        logs_filtered = [log for log in my_file_handler.read() if re.search(regex, log.msg)
                         and start_date_as_datetime <= log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_groupby_level_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.groupby_level(start_date=start_date, end_date=end_date)

    def test_groupby_level_works_with_no_input(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_level()
        log_dict = {}
        for log in my_file_handler.read():
            if log.level not in log_dict.keys():
                log_dict[log.level] = []
            log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_works_with_start_date_input(self):
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date)
        log_dict = {}
        for log in my_file_handler.read():
            if start_date_as_datetime <= log.date:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_returns_empty_dict_when_search_criteria_does_not_match_anything(self):
        start_date = "2025-06-25"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date)
        log_dict = {}
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader is not empty")

    def test_groupby_level_works_with_end_date_input(self):
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_level(end_date=end_date)
        log_dict = {}
        for log in my_file_handler.read():
            if log.date <= end_date_as_datetime:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_works_with_start_and_end_dates_input(self):
        start_date = "2021-06-20"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        end_date = "2021-07-13"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date, end_date=end_date)
        log_dict = {}
        for log in my_file_handler.read():
            if start_date_as_datetime <= log.date <= end_date_as_datetime:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.groupby_month(start_date=start_date, end_date=end_date)

    def test_groupby_month_works_with_no_input(self):
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_month()
        log_dict = {}
        for log in my_file_handler.read():
            if log.date.month not in log_dict.keys():
                log_dict[log.date.month] = []
            log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_works_with_start_date_input(self):
        start_date = "2021-06-23"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date)
        log_dict = {}
        for log in my_file_handler.read():
            if start_date_as_datetime <= log.date:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_returns_empty_dict_when_search_criteria_does_not_match_anything(self):
        start_date = "2025-06-25"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date)
        log_dict = {}
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader is not empty")

    def test_groupby_month_works_with_end_date_input(self):
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_month(end_date=end_date)
        log_dict = {}
        for log in my_file_handler.read():
            if log.date <= end_date_as_datetime:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_works_with_start_and_end_dates_input(self):
        start_date = "2021-06-20"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date, end_date=end_date)
        log_dict = {}
        for log in my_file_handler.read():
            if start_date_as_datetime <= log.date <= end_date_as_datetime:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")


class ProfilLoggerReaderCSVHandlerTest(unittest.TestCase):

    def setUp(self):
        global my_csv_handler
        my_csv_handler = CSVHandler("CSVHandler_sample_data.csv")

    def test_reader_saves_csv_handler_in_his_instance(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        self.assertTrue(my_reader.handler is my_csv_handler)

    def test_find_by_text_returns_empty_list_when_text_does_not_match_any_EntryLog_msg(self):
        text = "I like cup of tea in the morning"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_text(text=text)
        self.assertEqual(logs_returned, [],
                         "Reader didn't return empty list")

    def test_find_by_text_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.find_by_text(text="hopsa lala", start_date=start_date, end_date=end_date)

    def test_find_by_text_works_with_only_text_input(self):
        text = "debug"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_text(text=text)
        logs_filtered = [log for log in my_csv_handler.read() if text in log.msg]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_and_start_date_input(self):
        text = "info"
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_text(text=text, start_date=start_date)
        logs_filtered = [log for log in my_csv_handler.read() if text in log.msg
                         and start_date_as_datetime <= log.date]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_and_end_date_input(self):
        text = "warning"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_text(text=text, end_date=end_date)
        logs_filtered = [log for log in my_csv_handler.read() if text in log.msg
                         and log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_start_and_end_dates_input(self):
        text = "error"
        start_date = "2021-06-22"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_text(text=text, start_date=start_date, end_date=end_date)
        logs_filtered = [log for log in my_csv_handler.read() if text in log.msg
                         and start_date_as_datetime <= log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_returns_empty_list_when_text_does_not_match_any_EntryLog_msg(self):
        regex = r"\d"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_regex(regex=regex)
        self.assertEqual(logs_returned, [],
                         "Reader didn't return empty list")

    def test_find_by_regex_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.find_by_regex(regex="\d", start_date=start_date, end_date=end_date)

    def test_find_by_regex_works_with_only_regex_input(self):
        regex = r"[a-g] message"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_regex(regex=regex)
        logs_filtered = [log for log in my_csv_handler.read() if re.search(regex, log.msg)]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_and_start_date_input(self):
        regex = r"[l-m] message"
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, start_date=start_date)
        logs_filtered = [log for log in my_csv_handler.read() if re.search(regex, log.msg)
                         and start_date_as_datetime <= log.date]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_and_end_date_input(self):
        regex = r"[n-p] message"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, end_date=end_date)
        logs_filtered = [log for log in my_csv_handler.read() if re.search(regex, log.msg)
                         and log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_regex_works_with_text_start_and_end_dates_input(self):
        my_file_handler = FileHandler("FileHandler_sample_data.txt")
        regex = r"[r-z] message"
        start_date = "2021-06-22"
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_regex(regex=regex, start_date=start_date, end_date=end_date)
        logs_filtered = [log for log in my_file_handler.read() if re.search(regex, log.msg)
                         and start_date_as_datetime <= log.date <= end_date_as_datetime]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_groupby_level_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.groupby_level(start_date=start_date, end_date=end_date)

    def test_groupby_level_works_with_no_input(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_level()
        log_dict = {}
        for log in my_csv_handler.read():
            if log.level not in log_dict.keys():
                log_dict[log.level] = []
            log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_works_with_start_date_input(self):
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if start_date_as_datetime <= log.date:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_returns_empty_dict_when_search_criteria_does_not_match_anything(self):
        start_date = "2025-06-25"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date)
        log_dict = {}
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader is not empty")

    def test_groupby_level_works_with_end_date_input(self):
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_level(end_date=end_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if log.date <= end_date_as_datetime:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_level_works_with_start_and_end_dates_input(self):
        start_date = "2021-06-20"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        end_date = "2021-07-13"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_level(start_date=start_date, end_date=end_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if start_date_as_datetime <= log.date <= end_date_as_datetime:
                if log.level not in log_dict.keys():
                    log_dict[log.level] = []
                log_dict[log.level].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_raises_ValueError_when_start_date_is_later_than_end_date(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        start_date = "2021-06-25"
        end_date = "2021-06-22"
        with self.assertRaises(ValueError):
            my_reader.groupby_month(start_date=start_date, end_date=end_date)

    def test_groupby_month_works_with_no_input(self):
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_month()
        log_dict = {}
        for log in my_csv_handler.read():
            if log.date.month not in log_dict.keys():
                log_dict[log.date.month] = []
            log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_works_with_start_date_input(self):
        start_date = "2021-06-23"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if start_date_as_datetime <= log.date:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_returns_empty_dict_when_search_criteria_does_not_match_anything(self):
        start_date = "2025-06-25"
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date)
        log_dict = {}
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader is not empty")

    def test_groupby_month_works_with_end_date_input(self):
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_month(end_date=end_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if log.date <= end_date_as_datetime:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")

    def test_groupby_month_works_with_start_and_end_dates_input(self):
        start_date = "2021-06-20"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        end_date = "2021-06-25"
        end_date_as_datetime = datetime.datetime.fromisoformat(end_date)
        my_reader = ProfilLoggerReader(handler=my_csv_handler)
        logs_returned = my_reader.groupby_month(start_date=start_date, end_date=end_date)
        log_dict = {}
        for log in my_csv_handler.read():
            if start_date_as_datetime <= log.date <= end_date_as_datetime:
                if log.date.month not in log_dict.keys():
                    log_dict[log.date.month] = []
                log_dict[log.date.month].append(log)
        self.assertEqual(logs_returned, log_dict,
                         "Dict returned by Reader does not match dict created manually")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
