"""Exceptions raised by PyCacheMan."""


class PyCacheManError(Exception):
    """Base class for all exceptions raised by PyCacheMan."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        return
