"""
Exceptions module

    Custom exceptions to help you figure out where the automation broke.
"""

class OpsError(Exception):
    """Base class for exceptions in the ops module."""
    pass

class DaggerError(OpsError):
    """Base class for exceptions in the dagger module."""
    print(f'Something went {chr(0x1F4A9)} in your dagger code')
    pass


