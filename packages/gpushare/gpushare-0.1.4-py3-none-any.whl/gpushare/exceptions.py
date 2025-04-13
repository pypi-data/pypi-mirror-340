# gpushare/exceptions.py

class GPUShareError(Exception):
    """Base exception for gpushare."""
    pass

class AuthenticationError(GPUShareError):
    """Raised when login or token is invalid."""
    pass

class AuthorizationError(GPUShareError):
    """Raised when user lacks permission."""
    pass

class APIError(GPUShareError):
    """Raised on non‑200 API responses."""
    pass

