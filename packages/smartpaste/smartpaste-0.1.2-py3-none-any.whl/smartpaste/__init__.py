# -*- coding: utf-8 -*-
"""
SmartPaste: Reliable cross-platform clipboard pasting.

This __init__.py uses a trick to make the package itself callable.
So you can do:
import smartpaste
smartpaste("Hello")
"""

import sys
from .smartpaste import reliable_paste_text

__version__ = "0.1.2" # Increment version for change

class _SmartPasteCallable:
    """
    Internal class that holds the package version and makes the module
    callable, delegating the call to reliable_paste_text.
    It also allows access to the original function via attribute.
    """
    def __init__(self):
        self.__version__ = __version__
        # Expose the original function name as well
        self.reliable_paste_text = reliable_paste_text
        # Define what 'from smartpaste import *' imports (though not recommended)
        self.__all__ = ['reliable_paste_text']

    def __call__(self, text: str, delay_after_paste: float = 0.1):
        """
        Outputs the given text using the clipboard.

        Args:
            text (str): The text string to output.
            delay_after_paste (float): Pause after paste. Defaults to 0.1.
        """
        return reliable_paste_text(text, delay_after_paste)

# Replace the module object in sys.modules with an instance of our callable class
sys.modules[__name__] = _SmartPasteCallable()
