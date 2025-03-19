# This will be the functions for hashing and verifying passwords.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Hashes a password using the bcrypt algorithm. """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies a password against a hashed password. """
    return pwd_context.verify(plain_password, hashed_password)