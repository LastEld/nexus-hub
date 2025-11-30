"""
Script to create admin user.

Run this after initial migrations to create the first admin user.
"""

import asyncio
import sys
from getpass import getpass

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal
from core.security import hash_password
from domains.identity.models import User


async def create_admin_user():
    """Create admin user interactively."""
    print("🔐 NexusHub - Create Admin User\n")
    
    # Get user input
    email = input("Email: ").strip()
    username = input("Username: ").strip()
    full_name = input("Full Name (optional): ").strip() or None
    password = getpass("Password: ")
    password_confirm = getpass("Confirm Password: ")
    
    # Validate passwords match
    if password != password_confirm:
        print("❌ Passwords do not match!")
        sys.exit(1)
    
    # Validate minimum length
    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        sys.exit(1)
    
    # Hash password
    password_hash = hash_password(password)
    
    # Create user
    async with AsyncSessionLocal() as db:
        try:
            # Check if user exists
            from sqlalchemy import select
            result = await db.execute(
                select(User).where((User.email == email) | (User.username == username))
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"❌ User with email '{email}' or username '{username}' already exists!")
                sys.exit(1)
            
            # Create admin user
            admin_user = User(
                email=email,
                username=username,
                full_name=full_name,
                password_hash=password_hash,
                is_active=True,
                is_superuser=True,
                is_email_verified=True,
                roles=["super_admin", "admin"],
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            print(f"\n✅ Admin user created successfully!")
            print(f"   ID: {admin_user.id}")
            print(f"   Email: {admin_user.email}")
            print(f"   Username: {admin_user.username}")
            print(f"   Roles: {', '.join(admin_user.roles)}")
            
        except Exception as e:
            print(f"\n❌ Error creating admin user: {e}")
            await db.rollback()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_admin_user())
