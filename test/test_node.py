# tests/test_node.py

import unittest
from node.node import Node
from node.peer_protocol import PeerProtocol
from node.file_manager import FileManager

class TestNode(unittest.TestCase):
    def setUp(self):
        """Set up the Node instance and necessary components before each test."""
        self.node = Node()
        self.peer_protocol = PeerProtocol()
        self.file_manager = FileManager()

    def test_download_piece(self):
        """Test that the node can download a piece of a file from a peer."""
        result = self.node.download_piece('filehash123', 1)
        self.assertTrue(result)

    def test_upload_piece(self):
        """Test that the node can upload a piece of a file to a peer."""
        result = self.node.upload_piece('peer123', 'filehash123', 1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
