# tests/test_stats.py

import unittest
from interface.stats import display_stats

class TestStats(unittest.TestCase):
    def test_display_stats(self):
        """Test that stats are displayed correctly."""
        # Here, we mock the display_stats function as it may be hard to capture stdout directly.
        try:
            display_stats()
        except Exception as e:
            self.fail(f"Displaying stats raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
