"""
Script to generate secure random keys for SECRET_KEY and CSRF_SECRET.

Run this to generate production-ready secret keys.
"""

import secrets


def generate_secret_key(length: int = 64) -> str:
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(length)


if __name__ == "__main__":
    print("🔐 NexusHub - Secret Key Generator\n")
    print("Copy these to your .env file:\n")
    print(f"SECRET_KEY={generate_secret_key()}")
    print(f"CSRF_SECRET={generate_secret_key()}")
    print("\n⚠️  Keep these secret and never commit them to version control!")
