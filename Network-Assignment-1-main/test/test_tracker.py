# tests/test_tracker.py

import unittest
from tracker.tracker import Tracker
from tracker.database import PeerDatabase

class TestTracker(unittest.TestCase):
    def setUp(self):
        """Set up the Tracker instance and PeerDatabase before each test."""
        self.tracker = Tracker()
        self.peer_db = PeerDatabase()

    def test_announce_peer(self):
        """Test that the tracker successfully announces a new peer."""
        request = {
            'type': 'announce',
            'peer_id': 'peer123',
            'file_hash': 'filehash123',
            'pieces': ['piece1', 'piece2'],
        }
        response = self.tracker.handle_request(request)
        self.assertEqual(response['status'], 'success')

    def test_get_peers(self):
        """Test that the tracker correctly returns peers for a given file hash."""
        # Add peers to the database for the given file hash
        self.peer_db.add_peer('peer123', 'filehash123', ['piece1'])
        request = {'type': 'get_peers', 'file_hash': 'filehash123'}
        response = self.tracker.handle_request(request)
        self.assertIn('peer123', response['peers'])

if __name__ == '__main__':
    unittest.main()
