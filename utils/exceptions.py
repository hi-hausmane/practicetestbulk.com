# utils/exceptions.py - Custom Exception Classes

from fastapi import HTTPException, status


class TestGeniusException(Exception):
    """Base exception for all TestGenius errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(TestGeniusException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(TestGeniusException):
    """Raised when user doesn't have permission"""
    def __init__(self, message: str = "You don't have permission to perform this action"):
        super().__init__(message, status_code=403)


class ValidationError(TestGeniusException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class UsageLimitError(TestGeniusException):
    """Raised when user exceeds their usage quota"""
    def __init__(self, message: str = "You've exceeded your monthly usage limit"):
        super().__init__(message, status_code=429)


class ResourceNotFoundError(TestGeniusException):
    """Raised when a requested resource doesn't exist"""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404)


class GenerationError(TestGeniusException):
    """Raised when AI generation fails"""
    def __init__(self, message: str = "Question generation failed"):
        super().__init__(message, status_code=500)


class PaymentError(TestGeniusException):
    """Raised when payment processing fails"""
    def __init__(self, message: str = "Payment processing failed"):
        super().__init__(message, status_code=402)


class EmailNotVerifiedError(TestGeniusException):
    """Raised when user email is not verified"""
    def __init__(self, message: str = "Please verify your email before continuing"):
        super().__init__(message, status_code=403)


# Helper function to convert custom exceptions to FastAPI HTTPException
def to_http_exception(exception: TestGeniusException) -> HTTPException:
    """
    Convert a TestGeniusException to FastAPI HTTPException

    Args:
        exception: TestGeniusException instance

    Returns:
        HTTPException instance
    """
    return HTTPException(
        status_code=exception.status_code,
        detail=exception.message
    )


# Exception handler decorator
def handle_exceptions(func):
    """
    Decorator to automatically convert TestGeniusException to HTTPException
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TestGeniusException as e:
            raise to_http_exception(e)
        except Exception as e:
            # Log unexpected errors
            import logging
            logger = logging.getLogger("testgenius")
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again later."
            )

    return wrapper
