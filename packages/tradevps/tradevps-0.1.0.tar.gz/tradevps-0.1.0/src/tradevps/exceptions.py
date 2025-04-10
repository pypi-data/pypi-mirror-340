class TradeVPSException(Exception):
    """Base exception for TradeVPS client"""
    pass

class AuthenticationError(TradeVPSException):
    """Raised when authentication fails"""
    pass

class APIError(TradeVPSException):
    """Raised when API returns an error"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)