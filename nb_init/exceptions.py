"""Custom exceptions for nb-init."""


class NbInitError(Exception):
    """Base exception for nb-init.
    """
    pass



class ConnectionError(NbInitError):
    """Raised when connection to Netbox fails."""
    pass



class AuthenticationError(NbInitError):
    """Raised when authentication fails."""
    pass



class ValidationError(NbInitError):
    """Raised when input validation fails."""
    pass
