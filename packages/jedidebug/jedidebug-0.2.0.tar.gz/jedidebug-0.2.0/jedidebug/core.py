"""
Core functionality of the JediDebug library.
"""

import sys
import random
from .quotes import GENERAL_QUOTES, ERROR_QUOTES, ALL_QUOTES, ERROR_TYPE_MAP
from .handlers import jedi_exception_handler, jedi_function_decorator, original_excepthook


class JediDebug:
    """
    Main class for JediDebug functionality.
    """
    # Store the quotes for easy access
    QUOTES = GENERAL_QUOTES.copy()
    CATEGORIZED_QUOTES = ERROR_QUOTES.copy()
    
    # Flag to track activation status
    _active = False
    
    @classmethod
    def get_motivational_quote(cls):
        """
        Return a random Star Wars quote from the collection.
        
        Returns:
            str: A random motivational Star Wars quote.
        """
        return random.choice(cls.QUOTES)
    
    @classmethod
    def get_quote_by_category(cls, category):
        """
        Return a random Star Wars quote from a specific category.
        
        Args:
            category (str): The category of quote to retrieve.
            
        Returns:
            str: A random Star Wars quote from the specified category.
            
        Raises:
            ValueError: If the category does not exist.
        """
        if category in cls.CATEGORIZED_QUOTES and cls.CATEGORIZED_QUOTES[category]:
            return random.choice(cls.CATEGORIZED_QUOTES[category])
        else:
            available = ", ".join(sorted(cls.CATEGORIZED_QUOTES.keys()))
            raise ValueError(f"Unknown quote category: {category}. Available categories: {available}")
    
    @classmethod
    def add_quotes(cls, quotes):
        """
        Add custom quotes to the general quotes collection.
        
        Args:
            quotes (list): A list of quotes to add.
            
        Returns:
            int: The number of quotes added.
        """
        if not isinstance(quotes, list):
            quotes = [quotes]
        
        cls.QUOTES.extend(quotes)
        return len(quotes)
    
    @classmethod
    def add_categorized_quotes(cls, category, quotes):
        """
        Add custom quotes to a specific category.
        
        Args:
            category (str): The category to add quotes to.
            quotes (list): A list of quotes to add.
            
        Returns:
            int: The number of quotes added.
        """
        if not isinstance(quotes, list):
            quotes = [quotes]
        
        if category not in cls.CATEGORIZED_QUOTES:
            cls.CATEGORIZED_QUOTES[category] = []
        
        cls.CATEGORIZED_QUOTES[category].extend(quotes)
        return len(quotes)
    
    @classmethod
    def activate(cls):
        """
        Activate the JediDebug exception handler.
        
        Returns:
            bool: True if the activation was successful.
        """
        sys.excepthook = jedi_exception_handler
        cls._active = True
        print("JediDebug activated! May the Force guide your debugging journey.")
        return True
    
    @classmethod
    def deactivate(cls):
        """
        Deactivate the JediDebug exception handler.
        
        Returns:
            bool: True if the deactivation was successful.
        """
        sys.excepthook = original_excepthook
        cls._active = False
        print("JediDebug deactivated. The Force will be with you, always.")
        return True
    
    @classmethod
    def is_active(cls):
        """
        Check if JediDebug is active.
        
        Returns:
            bool: True if JediDebug is active, False otherwise.
        """
        return cls._active
    
    @classmethod
    def jedi_function(cls, func):
        """
        Decorator to provide Jedi wisdom if a function raises an exception.
        
        Args:
            func: The function to decorate
            
        Returns:
            The decorated function
        """
        return jedi_function_decorator(func)
    
    @classmethod
    def get_available_categories(cls):
        """
        Get a list of all available quote categories.
        
        Returns:
            list: A sorted list of available quote categories.
        """
        return sorted(cls.CATEGORIZED_QUOTES.keys())