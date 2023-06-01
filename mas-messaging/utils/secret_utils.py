from cryptography.fernet import Fernet


def get_decrypted_password(encrypted_password: str, key: str) -> str:
    """
    Decrypts a password using the provided key.

    Args:
        encrypted_password (str): The encrypted password to decrypt.
        key (str): The key used to decrypt the password.

    Returns:
        str: The decrypted password.
    """
    cipher_suite = Fernet(key)
    encoded_encrypted_password = encrypted_password.encode()

    return cipher_suite.decrypt(encoded_encrypted_password).decode()
