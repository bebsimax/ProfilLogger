import unittest
import os
import sys
import random

os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
src_path = (os.path.join(os.path.dirname(CUR_DIR), 'src'))
zad_rek_path = os.path.join(src_path, 'zad_rek')
sys.path.append(zad_rek_path)

from ProfilLogger import ProfilLogger

class ProfilLogerTest(unittest.TestCase):

    def setUp(self):
        global logger
        logger = ProfilLogger()

    def tearDown(self):
        try:
            os.remove('log.log')
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

    def test_info_always_creates_a_file(self):
        logger.info("test message")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)

        self.assertIn("log.log", files,
                      "Info method didn't create empty log.log file")

    def test_logger_can_save_message_to_file(self):
        logger.warning("This is your last warning")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(dir_path)
        self.assertIn("log.log", files,
                      "Warning method didn't create log.log file")
        with open ("log.log", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            self.assertEqual(lines[0], "This is your last warning")

    def test_logger_saves_all_log_levels_that_he_needs_to_save(self):
        levels = list(logger.levels.keys())
        selected_level = random.choice(levels)
        logger.set_log_level(selected_level)
        levels_to_write = [name for name in levels if logger.levels[selected_level] <= logger.levels[name]]
        for method in levels:
            class_method = getattr(logger, method)
            class_method(f"This is test message for {method}")
        with open("log.log", "r", newline="\n") as file:
            file_content = file.read()
            lines = file_content.splitlines()
            for method in levels_to_write:
                self.assertTrue(f"This is test message for {method}" in lines,
                                f"{method} didn't create a sample text")





if __name__ == '__main__':
    unittest.main(warnings='ignore')

