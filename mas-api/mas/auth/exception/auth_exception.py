class OAuth2EncryptionKeyNotFoundException(Exception):
    """
    Exception raised when a OAuth2 encryption key is not found in environment variables.
    """

    def __init__(
        self, message="OAuth2 Encryption Key not found in environment variables."
    ):
        self.message = message
        super().__init__(self.message)
