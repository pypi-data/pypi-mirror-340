"""Initialization

Initializes the Idiolect package and reexports its public API.
"""

# Import statements
from . import idioms

from .idioms import idiom

__all__ = ["idiom", "idioms"]
