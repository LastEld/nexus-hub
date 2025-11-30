"""
Permission-Based Access Control

RBAC (Role-Based Access Control) implementation.
"""

from enum import Enum
from typing import Optional


class Permission(str, Enum):
    """System permissions."""
    
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # CRM permissions
    CONTACT_READ = "contact:read"
    CONTACT_WRITE = "contact:write"
    CONTACT_DELETE = "contact:delete"
    
    COMPANY_READ = "company:read"
    COMPANY_WRITE = "company:write"
    COMPANY_DELETE = "company:delete"
    
    DEAL_READ = "deal:read"
    DEAL_WRITE = "deal:write"
    DEAL_DELETE = "deal:delete"
    
    # Project permissions
    PROJECT_READ = "project:read"
    PROJECT_WRITE = "project:write"
    PROJECT_DELETE = "project:delete"
    
    TASK_READ = "task:read"
    TASK_WRITE = "task:write"
    TASK_DELETE = "task:delete"
    
    # Team permissions
    TEAM_READ = "team:read"
    TEAM_WRITE = "team:write"
    TEAM_DELETE = "team:delete"
    
    # AI permissions
    AI_USE = "ai:use"
    AI_ADMIN = "ai:admin"
    
    # Plugin permissions
    PLUGIN_READ = "plugin:read"
    PLUGIN_INSTALL = "plugin:install"
    PLUGIN_MANAGE = "plugin:manage"
    
    # Admin permissions
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"
    SETTINGS_MANAGE = "settings:manage"
    AUDIT_READ = "audit:read"


class Role(str, Enum):
    """System roles with predefined permissions."""
    
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    USER = "user"
    GUEST = "guest"


# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.SUPER_ADMIN: list(Permission),  # All permissions
    
    Role.ADMIN: [
        Permission.USER_READ,
        Permission.USER_WRITE,
        Permission.CONTACT_READ,
        Permission.CONTACT_WRITE,
        Permission.CONTACT_DELETE,
        Permission.COMPANY_READ,
        Permission.COMPANY_WRITE,
        Permission.COMPANY_DELETE,
        Permission.DEAL_READ,
        Permission.DEAL_WRITE,
        Permission.DEAL_DELETE,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.PROJECT_DELETE,
        Permission.TASK_READ,
        Permission.TASK_WRITE,
        Permission.TASK_DELETE,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.TEAM_DELETE,
        Permission.AI_USE,
        Permission.PLUGIN_READ,
        Permission.PLUGIN_INSTALL,
        Permission.ADMIN_READ,
        Permission.SETTINGS_MANAGE,
        Permission.AUDIT_READ,
    ],
    
    Role.MANAGER: [
        Permission.USER_READ,
        Permission.CONTACT_READ,
        Permission.CONTACT_WRITE,
        Permission.COMPANY_READ,
        Permission.COMPANY_WRITE,
        Permission.DEAL_READ,
        Permission.DEAL_WRITE,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.TASK_READ,
        Permission.TASK_WRITE,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.AI_USE,
        Permission.PLUGIN_READ,
    ],
    
    Role.DEVELOPER: [
        Permission.USER_READ,
        Permission.CONTACT_READ,
        Permission.COMPANY_READ,
        Permission.DEAL_READ,
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.TASK_READ,
        Permission.TASK_WRITE,
        Permission.TEAM_READ,
        Permission.AI_USE,
        Permission.PLUGIN_READ,
    ],
    
    Role.USER: [
        Permission.USER_READ,
        Permission.CONTACT_READ,
        Permission.COMPANY_READ,
        Permission.DEAL_READ,
        Permission.PROJECT_READ,
        Permission.TASK_READ,
        Permission.TASK_WRITE,
        Permission.TEAM_READ,
        Permission.AI_USE,
    ],
    
    Role.GUEST: [
        Permission.PROJECT_READ,
        Permission.TASK_READ,
    ],
}


def get_role_permissions(role: Role) -> list[Permission]:
    """Get all permissions for a role."""
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(
    user_roles: list[str],
    required_permission: Permission,
) -> bool:
    """
    Check if user has a specific permission based on their roles.
    
    Args:
        user_roles: List of user role strings
        required_permission: Required permission
        
    Returns:
        True if user has the permission
    """
    for role_str in user_roles:
        try:
            role = Role(role_str)
            permissions = get_role_permissions(role)
            if required_permission in permissions:
                return True
        except ValueError:
            # Invalid role, skip
            continue
    
    return False


def get_user_permissions(user_roles: list[str]) -> set[Permission]:
    """
    Get all permissions for a user based on their roles.
    
    Args:
        user_roles: List of user role strings
        
    Returns:
        Set of all permissions
    """
    permissions: set[Permission] = set()
    
    for role_str in user_roles:
        try:
            role = Role(role_str)
            permissions.update(get_role_permissions(role))
        except ValueError:
            continue
    
    return permissions
