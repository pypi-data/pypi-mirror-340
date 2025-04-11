"""Idioms

Abstraction layers, decorators, wrappers, and other conveniences for
faster, more idiomatic prototyping workflows.
"""

# Import statements
import os

from collections.abc import Callable
from functools import wraps
from textwrap import dedent
from typing import Optional

from dotenv import load_dotenv


# Get value of `DEBUG` environment variable, which must be
# either `0` (false) or `1` (true).
load_dotenv()
DEBUG = bool(os.getenv("DEBUG"))


def idiom(*args,
          prep: Optional[Callable] = None,
          post: Optional[Callable] = None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if DEBUG:
                message = dedent(f"""
                    --------------------------------------------------------
                    DEBUGGING MESSAGE:

                    The `@idiom` decorator appears to have been applied to 
                    {fn.__name__}, which was called with the following args:

                    [Positional Arguments]
                    {args}

                    [Keyword Arguments]
                    {kwargs}

                    --------------------------------------------------------
                """).strip()
                print(message)

            # --- PREPROCESSOR ---
            if preprocessor:
                result = preprocessor(fn, args, kwargs)
                if result:
                    # Allow modification of args/kwargs
                    args, kwargs = result

            # --- ORIGINAL FUNCTION CALL ---
            result = fn(*args, **kwargs)

            # --- POSTPROCESSOR ---
            if postprocessor:
                post_result = postprocessor(fn, result, args, kwargs)
                if post_result is not None:
                    result = post_result

            return result
        return wrapper
    return decorator

