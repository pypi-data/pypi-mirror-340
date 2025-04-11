"""
Core functionality of the philosopherror library.
"""

import sys
import random
import warnings
from .philosophers import PHILOSOPHER_QUOTES
from .handlers import (
    original_excepthook,
    original_showwarning,
    philosophical_excepthook,
    philosophical_showwarning
)


def enable():
    """
    Enable philosophical error and warning messages.
    
    Returns:
        bool: True on success
    """
    sys.excepthook = philosophical_excepthook
    warnings.showwarning = philosophical_showwarning
    return True


def disable():
    """
    Disable philosophical error and warning messages.
    
    Returns:
        bool: True on success
    """
    sys.excepthook = original_excepthook
    warnings.showwarning = original_showwarning
    return True


def random_wisdom():
    """
    Get random philosophical wisdom.
    
    Returns:
        str: A random quote from a random philosopher
    """
    philosopher = random.choice(list(PHILOSOPHER_QUOTES.keys()))
    quote = random.choice(PHILOSOPHER_QUOTES[philosopher])
    return f"\"{quote}\"\n— {philosopher}"


def wisdom_from(philosopher):
    """
    Get wisdom from a specific philosopher.
    
    Args:
        philosopher (str): Name of the philosopher
        
    Returns:
        str: A random quote from the specified philosopher
        
    Raises:
        ValueError: If the philosopher is not in the database
    """
    if philosopher in PHILOSOPHER_QUOTES:
        quote = random.choice(PHILOSOPHER_QUOTES[philosopher])
        return f"\"{quote}\"\n— {philosopher}"
    else:
        available = ", ".join(sorted(PHILOSOPHER_QUOTES.keys()))
        raise ValueError(f"Unknown philosopher: {philosopher}. Available philosophers: {available}")


def list_philosophers():
    """
    List all available philosophers.
    
    Returns:
        list: Sorted list of all philosopher names
    """
    return sorted(PHILOSOPHER_QUOTES.keys())