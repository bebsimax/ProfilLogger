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
        # The operation didn't cause error, but his new and shiny log.log file is empty
        # He reads the help once again, only to find about the default setting for log entry is WARNING
        # He changes it to INFO using method set_log_level
        # my_logger.set_log_level("INFO")
        # He tries saving INFO log once again
        # my_logger.info("My first info message")
        # This time the file log.log contains his message
        self.fail("It's not over")

if __name__ == '__main__':
    unittest.main(warnings='ignore')




