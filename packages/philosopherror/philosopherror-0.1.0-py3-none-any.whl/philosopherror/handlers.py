"""
Contains handlers for exceptions and warnings.
"""

import sys
import functools
import traceback
import warnings
import random
from .philosophers import PHILOSOPHER_QUOTES, ERROR_PHILOSOPHER_MAP, DEFAULT_PHILOSOPHERS


class PhilosopherWarning(Warning):
    """Warning class for philosophical warnings."""
    pass


def get_philosophical_wisdom(error_type=None):
    """
    Get philosophical wisdom based on error type.
    
    Args:
        error_type (Exception, optional): Type of error. Defaults to None.
    
    Returns:
        str: A quote from a philosopher relevant to the error type.
    """
    if error_type and error_type in ERROR_PHILOSOPHER_MAP:
        philosophers = ERROR_PHILOSOPHER_MAP[error_type]
    else:
        philosophers = DEFAULT_PHILOSOPHERS
    
    philosopher = random.choice(philosophers)
    quote = random.choice(PHILOSOPHER_QUOTES[philosopher])
    
    return f"\n\n\"{quote}\"\n— {philosopher}\n"


def exception_handler(func):
    """
    Decorator to catch exceptions and provide philosophical wisdom.
    
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
            error_type = type(e)
            wisdom = get_philosophical_wisdom(error_type)
            
            # Print original traceback
            traceback.print_exc()
            
            # Print philosophical wisdom
            print(wisdom, file=sys.stderr)
            
            # Re-raise the original exception
            raise
    
    return wrapper


# Store the original excepthook and showwarning
original_excepthook = sys.excepthook
original_showwarning = warnings.showwarning


def philosophical_excepthook(exc_type, exc_value, exc_traceback):
    """
    Custom exception hook that adds philosophical wisdom.
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    original_excepthook(exc_type, exc_value, exc_traceback)
    wisdom = get_philosophical_wisdom(exc_type)
    print(wisdom, file=sys.stderr)


def philosophical_showwarning(message, category, filename, lineno, file=None, line=None):
    """
    Custom warning hook that adds philosophical wisdom.
    
    Args:
        message: Warning message
        category: Warning category
        filename: File where warning occurred
        lineno: Line number where warning occurred
        file: File to write warning to
        line: Line of source code where warning occurred
    """
    original_showwarning(message, category, filename, lineno, file, line)
    wisdom = get_philosophical_wisdom(Warning)
    print(wisdom, file=sys.stderr if file is None else file)