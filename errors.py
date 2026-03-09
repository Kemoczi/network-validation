class NetworkValidationError(Exception):
    """Base class for errors."""


class InvalidPortError(NetworkValidationError):
    """Raised when user provides an invalid port number."""


class UnknownCommandError(NetworkValidationError):
    """Raised when an unsupported command is requested."""


class ResponseReadError(NetworkValidationError):
    """Raised when response cannot be read."""


class ResponseFormatError(NetworkValidationError):
    """Raised when the response format is not what parser expects."""


class PortNotFoundError(NetworkValidationError):
    """Raised when requested port is not present in the response."""

class InvalidModeError(NetworkValidationError):
    """Raised when user provides an invalid mode."""