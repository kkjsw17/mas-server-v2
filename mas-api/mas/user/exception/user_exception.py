class UserNotFoundException(Exception):
    """
    Exception raised when a user is not found in the system.
    """

    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
