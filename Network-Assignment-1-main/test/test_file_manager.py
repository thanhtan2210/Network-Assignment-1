# tests/test_file_manager.py

import unittest
from node.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        """Set up the FileManager instance before each test."""
        self.file_manager = FileManager()

    def test_read_piece(self):
        """Test that a piece of a file can be read correctly."""
        data = self.file_manager.read_piece('filehash123', 1)
        self.assertIsNotNone(data)

    def test_write_piece(self):
        """Test that a piece of a file can be written to disk."""
        result = self.file_manager.write_piece('filehash123', 1, b'piece_data')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
