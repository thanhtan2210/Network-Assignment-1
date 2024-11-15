# tests/test_metainfo.py

import unittest
from common.metainfo import Metainfo

class TestMetainfo(unittest.TestCase):
    def setUp(self):
        """Set up the Metainfo instance before each test."""
        self.metainfo = Metainfo()

    def test_parse_torrent(self):
        """Test that a torrent file can be parsed correctly."""
        result = self.metainfo.parse_torrent('path_to_torrent_file.torrent')
        self.assertTrue(result)

    def test_get_file_hash(self):
        """Test that the file hash can be extracted correctly from the .torrent file."""
        file_hash = self.metainfo.get_file_hash('path_to_torrent_file.torrent')
        self.assertEqual(file_hash, 'expected_file_hash')

if __name__ == '__main__':
    unittest.main()
