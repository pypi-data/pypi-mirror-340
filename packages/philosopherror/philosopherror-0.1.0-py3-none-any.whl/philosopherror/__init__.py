"""
philosopherror - A silly yet insightful Python library that provides
philosophical wisdom when errors and warnings occur.
"""

__version__ = "0.1.0"
__author__ = "Not a Real Programmer"
__email__ = "notarealprogrammer010@gmail.com"
__license__ = "MIT"

from .core import (
    enable,
    disable,
    random_wisdom,
    wisdom_from,
    list_philosophers
)

from .handlers import (
    exception_handler,
    PhilosopherWarning,
    get_philosophical_wisdom
)

# Auto-enable when imported
enable()