# tests/test_peer_protocol.py

import unittest
from node.peer_protocol import PeerProtocol

class TestPeerProtocol(unittest.TestCase):
    def setUp(self):
        """Set up the PeerProtocol instance before each test."""
        self.peer_protocol = PeerProtocol()

    def test_send_piece(self):
        """Test that a piece can be sent to a peer."""
        result = self.peer_protocol.send_piece('peer123', 'filehash123', 1)
        self.assertTrue(result)

    def test_receive_piece(self):
        """Test that a piece can be received from a peer."""
        result = self.peer_protocol.receive_piece('peer123', 'filehash123', 1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
