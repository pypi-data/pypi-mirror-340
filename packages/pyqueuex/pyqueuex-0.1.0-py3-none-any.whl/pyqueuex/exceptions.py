class QueueXError(Exception):
    """Base exception for QueueX errors."""
    pass

class QueueNotFoundError(QueueXError):
    """Raised when a queue is not found."""
    pass

class JobProcessingError(QueueXError):
    """Raised when job processing fails."""
    pass