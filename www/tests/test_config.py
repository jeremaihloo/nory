import unittest

from infrastructures.configs import load_config_from_command_line


class MyTestCase(unittest.TestCase):
    def test_something(self):
        load_config_from_command_line()
        pass


if __name__ == '__main__':
    unittest.main()
