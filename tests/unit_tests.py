import unittest
import os
import sys
import random

os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
src_path = (os.path.join(os.path.dirname(CUR_DIR), 'src'))
zad_rek_path = os.path.join(src_path, 'zad_rek')
sys.path.append(zad_rek_path)

from ProfilLogger import ProfilLogger, FileHandler, LogEntry


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
        with open ("log.txt", "r", newline="\n") as file:
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
        import datetime
        now = datetime.datetime.now()
        my_log = LogEntry("this is message", "this is level")
        formated_now = now.strftime("%b %d %Y %H:%M:%S")
        file_handler.save(my_log)
        with open ("log.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            lines = [component.strip() for component in lines[0].split(";")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formated_now,
                         "FileHandler didn't save date")
        self.assertEqual(msg, "this is message",
                         "FileHandler didn't save msg")
        self.assertEqual(level, "this is level",
                         "FileHandler didn't save level")

    def test_file_handler_creates_log_with_specified_name(self):
        import datetime
        now = datetime.datetime.now()
        my_log = LogEntry("this is message", "this is level")
        formated_now = now.strftime("%b %d %Y %H:%M:%S")
        file_handler = FileHandler("sample.txt")
        file_handler.save(my_log)
        with open("sample.txt", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            lines = [component.strip() for component in lines[0].split(";")]
            date, level, msg = tuple(lines)

        self.assertEqual(date, formated_now,
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


class LogEntryTest(unittest.TestCase):

    def test_LogEntry_stores_user_message(self):
        message = "I am logging"
        entry = LogEntry(message)
        self.assertEqual(message, entry.msg,
                         "LogEntry didn't store message")

    def test_LogEntry_stores_level(self):
        message = "Boxes"
        level = "info"
        entry = LogEntry(message, level)
        self.assertEqual(entry.level, level,
                         "LogEntry didn't store level")

    def test_LogEntry_stores_datetime(self):
        import datetime
        now = datetime.datetime.now()
        formated_now = now.strftime("%b %d %Y %H:%M:%S")
        message = "I am logging"
        entry = LogEntry(message)
        data_from_log = entry.date
        self.assertEqual(data_from_log, formated_now)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

