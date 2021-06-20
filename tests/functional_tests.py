import unittest

class NewUserTest(unittest.TestCase):


    def test_user_can_create_logger(self):
        # Jan is a careful developer who prefers logging over print statements
        # He has heard about new custom logger called ProfilLogger
        # He quickly imports it inside his working file
        from src.zad_rek.ProfilLogger import ProfilLogger
        # Jan creates instance of ProfilLogger called my_logger
        my_logger = ProfilLogger()
        self.assertIsInstance(my_logger, ProfilLogger)
    # Before logging his current work he decides to test the new logger
    # But, he has no idea how it works
    # He checks the docstring
    # It contains information about the class and it's methods
    # Happy with the new lecture Jan starts to read
    # He finds about the info method
    # Jan decides to try it on his new object


if __name__ == '__main__':
    unittest.main(warnings='ignore')





