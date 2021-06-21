import unittest
import os
import sys
# Jan is a careful developer who prefers logging over print statements
# He has heard about new custom logger called ProfilLogger
# He quickly imports it inside his working file


os.chdir(os.path.dirname(__file__))
CUR_DIR = os.getcwd()
src_path = (os.path.join(os.path.dirname(CUR_DIR), 'src'))
zad_rek_path = os.path.join(src_path, 'zad_rek')
sys.path.append(zad_rek_path)

from ProfilLogger import ProfilLogger


class CreationTest(unittest.TestCase):

    def test_user_can_create_logger(self):
        # Jan creates instance of ProfilLogger called my_logger
        my_logger = ProfilLogger()
        self.assertIsInstance(my_logger, ProfilLogger)


class UsageTest(unittest.TestCase):

    def setUp(self):
        global my_logger
        my_logger = ProfilLogger()

    def tearDown(self):
        try:
            os.remove('log.log')
        except OSError as error:
            print(error)
            print("log.log NOT REMOVED")

    def test_logger_always_creates_a_file(self):
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

        self.assertIn("log.log", files,
                      "Info method didn't create empty log.log file")
        # The operation didn't cause error, and he noticed empty log.log file in his working directory
        with open ("log.log", "r") as file:

            file_content = file.read()

            self.assertEqual(file_content, '',
                            "Info created not empty log.log file")

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
        self.assertIn("log.log", files,
                      "Info method didn't create log.log file")

        # This time the file log.log contains his message
        with open ("log.log", "r") as file:
            whole_text = file.read()
            lines = whole_text.splitlines()

            self.assertTrue("My first info message" in lines,
                            "info didn't save message to file")


        # He adds warning level message to his log
        my_logger.warning("My first warning message")

        # He checks if it created a new enrty in his log.log file
        with open("log.log", "r") as file:
            whole_text = file.read()
            lines = whole_text.splitlines()
            self.assertTrue("My first warning message" in lines,
                             "warning didn't save message to file")


if __name__ == '__main__':
    unittest.main(warnings='ignore')




