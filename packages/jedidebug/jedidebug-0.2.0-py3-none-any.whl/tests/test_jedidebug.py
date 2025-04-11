"""
Tests for the JediDebug package.
"""

import sys
import unittest
import io
from contextlib import redirect_stderr

from jedidebug import JediDebug
from jedidebug.quotes import GENERAL_QUOTES, ERROR_QUOTES


class TestJediDebug(unittest.TestCase):
    """Test cases for JediDebug package."""

    def setUp(self):
        """Set up for tests."""
        # Make sure JediDebug is activated
        JediDebug.activate()

    def tearDown(self):
        """Clean up after tests."""
        # Reset to original state after each test
        JediDebug.deactivate()

    def test_activate_deactivate(self):
        """Test activating and deactivating JediDebug."""
        # Test activate
        original_excepthook = sys.excepthook
        
        JediDebug.activate()
        self.assertNotEqual(sys.excepthook, original_excepthook)
        self.assertTrue(JediDebug.is_active())
        
        # Test deactivate
        JediDebug.deactivate()
        self.assertEqual(sys.excepthook, original_excepthook)
        self.assertFalse(JediDebug.is_active())

    def test_get_motivational_quote(self):
        """Test getting a random motivational quote."""
        quote = JediDebug.get_motivational_quote()
        self.assertIsInstance(quote, str)
        self.assertGreater(len(quote), 10)  # Quote should be non-empty
        self.assertTrue(quote in JediDebug.QUOTES)

    def test_get_quote_by_category(self):
        """Test getting a quote by category."""
        # Test with a valid category
        if 'syntax' in JediDebug.CATEGORIZED_QUOTES and JediDebug.CATEGORIZED_QUOTES['syntax']:
            quote = JediDebug.get_quote_by_category('syntax')
            self.assertIsInstance(quote, str)
            self.assertGreater(len(quote), 10)
            self.assertTrue(quote in JediDebug.CATEGORIZED_QUOTES['syntax'])
        
        # Test with an invalid category
        with self.assertRaises(ValueError):
            JediDebug.get_quote_by_category('not_a_real_category')

    def test_add_quotes(self):
        """Test adding custom quotes."""
        # Initial count
        initial_count = len(JediDebug.QUOTES)
        
        # Add a single quote
        new_quote = "This is a test quote from a galaxy far, far away."
        num_added = JediDebug.add_quotes(new_quote)
        self.assertEqual(num_added, 1)
        self.assertEqual(len(JediDebug.QUOTES), initial_count + 1)
        self.assertIn(new_quote, JediDebug.QUOTES)
        
        # Add multiple quotes
        new_quotes = ["Test quote 1", "Test quote 2", "Test quote 3"]
        num_added = JediDebug.add_quotes(new_quotes)
        self.assertEqual(num_added, 3)
        self.assertEqual(len(JediDebug.QUOTES), initial_count + 4)
        for quote in new_quotes:
            self.assertIn(quote, JediDebug.QUOTES)

    def test_add_categorized_quotes(self):
        """Test adding categorized quotes."""
        # Test adding to existing category
        category = 'syntax'
        if category in JediDebug.CATEGORIZED_QUOTES:
            initial_count = len(JediDebug.CATEGORIZED_QUOTES[category])
            new_quote = "This is a new test quote for syntax errors."
            num_added = JediDebug.add_categorized_quotes(category, new_quote)
            self.assertEqual(num_added, 1)
            self.assertEqual(len(JediDebug.CATEGORIZED_QUOTES[category]), initial_count + 1)
            self.assertIn(new_quote, JediDebug.CATEGORIZED_QUOTES[category])
        
        # Test adding to new category
        new_category = 'test_category'
        if new_category not in JediDebug.CATEGORIZED_QUOTES:
            new_quotes = ["Test category quote 1", "Test category quote 2"]
            num_added = JediDebug.add_categorized_quotes(new_category, new_quotes)
            self.assertEqual(num_added, 2)
            self.assertIn(new_category, JediDebug.CATEGORIZED_QUOTES)
            self.assertEqual(len(JediDebug.CATEGORIZED_QUOTES[new_category]), 2)
            for quote in new_quotes:
                self.assertIn(quote, JediDebug.CATEGORIZED_QUOTES[new_category])

    def test_is_active(self):
        """Test the is_active function."""
        JediDebug.activate()
        self.assertTrue(JediDebug.is_active())
        
        JediDebug.deactivate()
        self.assertFalse(JediDebug.is_active())

    def test_jedi_function_decorator(self):
        """Test the jedi_function decorator."""
        @JediDebug.jedi_function
        def function_that_raises():
            """Function that will raise an error."""
            raise ValueError("Test error")

        # Capture stderr to check for Jedi wisdom
        err = io.StringIO()
        with redirect_stderr(err):
            try:
                function_that_raises()
            except ValueError:
                pass

        output = err.getvalue()
        self.assertIn("JEDI FUNCTION GUIDANCE", output)
        self.assertIn("🌟", output)
        self.assertIn("function_that_raises", output)

    def test_exception_handler(self):
        """Test the exception handler with various errors."""
        # Activate JediDebug
        JediDebug.activate()
        
        # Test with ValueError
        err = io.StringIO()
        with redirect_stderr(err):
            try:
                int("not a number")
            except ValueError:
                pass

        output = err.getvalue()
        self.assertIn("JEDI WISDOM", output)
        self.assertIn("🌟", output)
        self.assertIn("ValueError", output)
        
        # Clear buffer
        err = io.StringIO()
        
        # Test with TypeError
        with redirect_stderr(err):
            try:
                len(5)
            except TypeError:
                pass

        output = err.getvalue()
        self.assertIn("JEDI WISDOM", output)
        self.assertIn("🌟", output)
        self.assertIn("TypeError", output)

    def test_get_available_categories(self):
        """Test getting available categories."""
        categories = JediDebug.get_available_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        self.assertEqual(sorted(categories), categories)  # Check that list is sorted
        
        # Check all categories are valid
        for category in categories:
            self.assertIn(category, JediDebug.CATEGORIZED_QUOTES)


if __name__ == "__main__":
    unittest.main()