"""
Tests for the philosopherror package.
"""

import sys
import unittest
import warnings
import io
from contextlib import redirect_stderr

import philosopherror
from philosopherror.philosophers import PHILOSOPHER_QUOTES


class TestPhilosopherror(unittest.TestCase):
    """Test cases for philosopherror package."""

    def setUp(self):
        """Set up for tests."""
        # Make sure philosophical errors are enabled
        philosopherror.enable()

    def tearDown(self):
        """Clean up after tests."""
        # Reset to original hooks after each test
        philosopherror.disable()

    def test_enable_disable(self):
        """Test enabling and disabling the philosophical errors."""
        # Test enable
        original_excepthook = sys.excepthook
        original_showwarning = warnings.showwarning
        
        philosopherror.enable()
        self.assertNotEqual(sys.excepthook, original_excepthook)
        self.assertNotEqual(warnings.showwarning, original_showwarning)
        
        # Test disable
        philosopherror.disable()
        self.assertEqual(sys.excepthook, original_excepthook)
        self.assertEqual(warnings.showwarning, original_showwarning)

    def test_random_wisdom(self):
        """Test getting random wisdom."""
        wisdom = philosopherror.random_wisdom()
        self.assertIsInstance(wisdom, str)
        self.assertGreater(len(wisdom), 10)  # Wisdom should be non-empty
        
        # Check that the wisdom contains a quote and a philosopher
        parts = wisdom.split("\n— ")
        self.assertEqual(len(parts), 2)
        self.assertTrue(parts[0].startswith('"') and parts[0].endswith('"'))
        self.assertTrue(parts[1] in PHILOSOPHER_QUOTES)

    def test_wisdom_from(self):
        """Test getting wisdom from a specific philosopher."""
        # Test with a valid philosopher
        philosopher = "Socrates"
        wisdom = philosopherror.wisdom_from(philosopher)
        self.assertIsInstance(wisdom, str)
        self.assertGreater(len(wisdom), 10)
        self.assertTrue(f"— {philosopher}" in wisdom)
        
        # Test with an invalid philosopher
        with self.assertRaises(ValueError):
            philosopherror.wisdom_from("Not A Philosopher")

    def test_list_philosophers(self):
        """Test listing all philosophers."""
        philosophers = philosopherror.list_philosophers()
        self.assertIsInstance(philosophers, list)
        self.assertGreater(len(philosophers), 0)
        self.assertEqual(len(philosophers), len(PHILOSOPHER_QUOTES))
        self.assertEqual(sorted(philosophers), philosophers)  # Check that list is sorted

    def test_exception_handler_decorator(self):
        """Test the exception handler decorator."""
        @philosopherror.exception_handler
        def function_that_raises():
            raise ValueError("Test error")

        # Capture stderr to check for philosophical quote
        err = io.StringIO()
        with redirect_stderr(err):
            try:
                function_that_raises()
            except ValueError:
                pass

        output = err.getvalue()
        self.assertIn("Traceback", output)
        self.assertIn("ValueError: Test error", output)
        self.assertIn("—", output)  # Philosopher attribution marker

    def test_warning(self):
        """Test philosophical wisdom on warnings."""
        # Capture stderr to check for philosophical quote
        err = io.StringIO()
        with redirect_stderr(err):
            warnings.warn("Test warning")

        output = err.getvalue()
        self.assertIn("Test warning", output)
        self.assertIn("—", output)  # Philosopher attribution marker

    def test_get_philosophical_wisdom(self):
        """Test getting philosophical wisdom for an error type."""
        wisdom = philosopherror.get_philosophical_wisdom(ValueError)
        self.assertIsInstance(wisdom, str)
        self.assertGreater(len(wisdom), 10)
        self.assertIn("—", wisdom)  # Philosopher attribution marker


if __name__ == "__main__":
    unittest.main()