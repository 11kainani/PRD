import unittest
from file_manager import FileManager

class TestFileManager(unittest.TestCase):

    def test_file_manager_init(self):
        file_manager = FileManager("data/519a0d18-032d-4027-bd7f-21a1c39e8d89.csv")
        self.assertIsNotNone(file_manager)
        self.assertEqual(file_manager.main_file, "data/519a0d18-032d-4027-bd7f-21a1c39e8d89.csv")


if __name__ == '__main__':
    test = TestFileManager()
    test.test_file_manager_init()