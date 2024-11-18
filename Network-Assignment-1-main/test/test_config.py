# tests/test_config.py

import unittest
from interface.config import CONFIG

class TestConfig(unittest.TestCase):
    def test_config_values(self):
        """Test that configuration values are loaded correctly."""
        self.assertEqual(CONFIG['tracker_host'], '127.0.0.1')
        self.assertEqual(CONFIG['tracker_port'], 6881)
        self.assertEqual(CONFIG['max_peers'], 10)

if __name__ == '__main__':
    unittest.main()
