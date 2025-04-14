class ApostrofoApiError(Exception):
    """Base exception for all API errors"""
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(ApostrofoApiError):
    """Raised when there is an authentication error"""
    pass


class InvalidRequestError(ApostrofoApiError):
    """Raised when the request is invalid"""
    pass


class ApiConnectionError(ApostrofoApiError):
    """Raised when there is a connection error"""
    pass


class RateLimitError(ApostrofoApiError):
    """Raised when rate limit is exceeded"""
    pass


class ServiceError(ApostrofoApiError):
    """Raised when there is a server error"""
    pass