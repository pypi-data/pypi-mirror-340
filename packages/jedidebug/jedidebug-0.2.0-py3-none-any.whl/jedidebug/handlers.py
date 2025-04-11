"""
Contains handlers for exceptions and decorators.
"""

import sys
import traceback
import functools
import random
from .quotes import GENERAL_QUOTES, ERROR_QUOTES, ERROR_TYPE_MAP


def get_quote_for_error(error_type=None):
    """
    Get a quote appropriate for the given error type.
    
    Args:
        error_type (str, optional): The error type name. Defaults to None.
        
    Returns:
        tuple: A tuple containing the main quote and an encouragement quote.
    """
    # Get main quote based on error type if possible
    if error_type and error_type in ERROR_TYPE_MAP:
        category = ERROR_TYPE_MAP[error_type]
        if category in ERROR_QUOTES and ERROR_QUOTES[category]:
            main_quote = random.choice(ERROR_QUOTES[category])
        else:
            main_quote = random.choice(GENERAL_QUOTES)
    else:
        main_quote = random.choice(GENERAL_QUOTES)
    
    # Get an encouragement quote
    encouragement = random.choice(ERROR_QUOTES.get('encouragement', ['Trust your instincts, young Padawan.']))
    
    return main_quote, encouragement


def jedi_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler that adds Star Wars quotes.
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    # Print the original traceback
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)), file=sys.stderr)
    
    # Get Jedi wisdom based on the error type
    main_quote, encouragement = get_quote_for_error(exc_type.__name__)
    
    # Add the motivational quotes
    print("\n✨ JEDI WISDOM ✨", file=sys.stderr)
    print(f"🌟 {main_quote}", file=sys.stderr)
    print(f"🌟 {encouragement}\n", file=sys.stderr)


def jedi_function_decorator(func):
    """
    Decorator to provide Jedi wisdom if a function raises an exception.
    
    Args:
        func: The function to decorate
        
    Returns:
        The decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = type(e).__name__
            main_quote, encouragement = get_quote_for_error(error_type)
            
            print(f"\n✨ JEDI FUNCTION GUIDANCE ✨", file=sys.stderr)
            print(f"🌟 {main_quote}", file=sys.stderr)
            print(f"🌟 The function '{func.__name__}' requires your attention, it does.", file=sys.stderr)
            print(f"🌟 {encouragement}\n", file=sys.stderr)
            
            # Re-raise the exception for normal handling
            raise
    
    return wrapper


# Store the original excepthook
original_excepthook = sys.excepthook