import unittest
import os
import sys
import random
import datetime
os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
src_path = (os.path.join(os.path.dirname(CUR_DIR), 'src'))
zad_rek_path = os.path.join(src_path, 'zad_rek')
sys.path.append(zad_rek_path)

from ProfilLogger import ProfilLogger, FileHandler, LogEntry, ProfilLoggerReader


class ProfilLoggerTest(unittest.TestCase):

    def setUp(self):
        global logger
        logger = ProfilLogger(handlers=[FileHandler()])

    def tearDown(self):
        try:
            os.remove('log.txt')
        except OSError as error:
            #print(error)
            #print("log.log NOT REMOVED")
            pass

    def test_logger_has_default_warning_level(self):
        self.assertEqual(logger.log_level, "warning",
                         "warning is not default log level")

    def test_set_log_level_method_changes_log_level(self):
        logger.set_log_level("info")
        self.assertEqual(logger.log_level, "info",
                         "set_log_method didn't change log level")

    def test_set_log_level_method_does_not_change_level_when_input_is_not_known(self):
        logger.set_log_level("WE DO IT LIVE")
        self.assertEqual(logger.log_level, "warning",
                         "set_log_method changed log level after receiving invalid input")

    def test_logger_can_save_message_to_file(self):
        logger.warning("This is your last warning")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertIn("log.txt", files,
                      "Warning method didn't create log.log file")
        with open("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            self.assertTrue( "This is your last warning" in lines[0],
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

    def test_logger_raises_TypeError_when_passed_wrong_type_as_Handler(self):
        with self.assertRaises(TypeError):
            ProfilLogger(handlers=[11])
            ProfilLogger(handlers=["log.txt"])

    def test_logger_can_save_to_two_txt_files_at_once(self):
        import datetime
        first_handler = FileHandler("first.txt")
        second_handler = FileHandler("second.txt")
        my_logger = ProfilLogger(handlers=[first_handler, second_handler])
        now = datetime.datetime.now()
        my_logger.warning("Are you still there?")
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
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
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
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
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
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
        now = datetime.datetime.now()
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
        message = "I am logging"
        level = "debug"
        entry = LogEntry(message, level)
        data_from_log = entry.date
        self.assertEqual(data_from_log, formatted_now)

    def test_printed_LogEntry_returns_correct_text(self):
        msg = "The message"
        level = "info"
        now = datetime.datetime.now()
        entry = LogEntry(msg, level=level)
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
        self.assertEqual(entry.__str__(), f"{formatted_now} ; {level} ; {msg}",
                         "LogEntry does not print the way it should")

    def test_LogEntries_date_can_be_compared_to_other_dates(self):
        now = datetime.datetime.now()
        log = LogEntry(msg="Msg", level="info")
        formatted_now = now.strftime("%b %d %Y %H:%M:%S")
        self.assertTrue(log.date <= formatted_now)


class ProfilLoggerReaderTest(unittest.TestCase):

    def test_logger_reader_cannot_be_created_without_passing_an_argument(self):
        with self.assertRaises(TypeError):
            ProfilLoggerReader()

    def test_logger_reader_cannot_be_created_without_valid_handler(self):
        with self.assertRaises(TypeError):
            ProfilLoggerReader(handler="log.txt")

    def test_logger_reader_rises_TypeError_when_receiving_more_than_one_handler(self):
        first = FileHandler("first.txt")
        second = FileHandler("second.txt")
        with self.assertRaises(TypeError):
            ProfilLoggerReader(handler=[first, second])

    def test_logger_reader_can_be_created_with_correct_handler(self):
        my_handler = FileHandler("logs.txt")
        my_logger_reader = ProfilLoggerReader(my_handler)
        self.assertTrue(isinstance(my_logger_reader, ProfilLoggerReader))

    def test_find_by_text_works_wth_file_handler(self):
        my_file_handler = FileHandler("FileHandler_sample_data.txt")
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        self.assertTrue(my_reader.handler is my_file_handler)

    def test_find_by_text_works_with_only_text_input(self):
        my_file_handler = FileHandler("FileHandler_sample_data.txt")
        text = "debug"
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text)
        all_logs = my_file_handler.read()
        logs_filtered = [log for log in all_logs if text in log.msg]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")

    def test_find_by_text_works_with_text_and_start_date_input(self):
        my_file_handler = FileHandler("FileHandler_sample_data.txt")
        text = "info"
        start_date = "2021-06-25"
        start_date_as_datetime = datetime.datetime.fromisoformat(start_date)
        my_reader = ProfilLoggerReader(handler=my_file_handler)
        logs_returned = my_reader.find_by_text(text=text, start_date=start_date)
        all_logs = my_file_handler.read()
        logs_filtered = [log for log in all_logs if text in log.msg and start_date_as_datetime <= log.date]
        self.assertEqual(logs_returned, logs_filtered,
                         "Logs returned by Reader does not match logs filtered manually")



if __name__ == '__main__':
    unittest.main(warnings='ignore')

