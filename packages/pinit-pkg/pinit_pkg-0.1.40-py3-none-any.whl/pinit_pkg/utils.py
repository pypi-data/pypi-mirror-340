import jwt as pkg_jwt
import random
import re
import string
import unicodedata


def generate_random_string(length: int) -> str:
    """Generate a random string with the specified length.
    The string will contain uppercase and lowercase letters, and numbers.

    Args:
        length (int): The length of the string to generate

    Returns:
        str: A random string of the specified length
    """
    # Define the character set: letters (upper and lower) and digits
    chars = string.ascii_letters + string.digits

    # Generate random string using random.choices
    return ''.join(random.choices(chars, k=length))


def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from the given text.
    The function will:
    1. Convert to lowercase
    2. Remove accents
    3. Replace spaces with hyphens
    4. Remove special characters
    5. Remove multiple hyphens

    Args:
        text (str): The text to convert to a slug

    Returns:
        str: A URL-friendly slug
    """
    # Convert to lowercase and normalize unicode characters
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # Replace any non-alphanumeric character with a hyphen
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    return text


def get_jwt_headers(token: str) -> dict:
    """Get JWT headers without verifying signature.

    Args:
        token (str): JWT token

    Returns:
        dict: Token headers including typ, alg, and kid
    """
    return pkg_jwt.get_unverified_header(token)


def get_jwt_payload(token: str) -> dict:
    """Get JWT payload without verifying signature.

    Args:
        token (str): JWT token

    Returns:
        dict: Token payload
    """
    return pkg_jwt.decode(token, options={"verify_signature": False})
