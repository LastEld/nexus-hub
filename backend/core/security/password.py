"""
Password Hashing with Argon2

More secure than bcrypt for modern applications.
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from ..config import settings

# Initialize Argon2 password hasher
ph = PasswordHasher(
    time_cost=settings.PASSWORD_HASH_TIME_COST,
    memory_cost=settings.PASSWORD_HASH_MEMORY_COST,
    parallelism=settings.PASSWORD_HASH_PARALLELISM,
)


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        ph.verify(hashed_password, plain_password)
        
        # Check if rehashing is needed (parameters changed)
        if ph.check_needs_rehash(hashed_password):
            # In a real application, you would update the hash here
            pass
        
        return True
    except (VerificationError, VerifyMismatchError, InvalidHashError):
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    Check if a password hash needs to be rehashed.
    
    Args:
        hashed_password: Hashed password
        
    Returns:
        True if rehashing is needed
    """
    try:
        return ph.check_needs_rehash(hashed_password)
    except Exception:
        return True
