#!/usr/bin/python3
"""
The permission classes defined in this module
"""

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.basemodel import BaseModel, Base
from models.role import Role


class Permission(BaseModel, Base):
    """
    The Permission class represents permissions for each role.

    Args:
        permission_name (str): The name of the permission.
        role_id (str): The ID of the role associated with the permission.
        assigned_user_id (str): The ID of the user to whom the permission is assigned.
        permission_desc (str, optional): The description of the permission.
        access_level (int, optional): The access level of the permission.

    Attributes:
        permission_name (str): The name of the permission.
        permission_desc (str): The description of the permission.
        role_id (str): The ID of the role associated with the permission.
        assigned_user_id (str): The ID of the user to whom the permission is assigned.
        access_level (int): The access level of the permission.
    """

    __tablename__ = 'permissions'

    permission_name = Column(String(50), unique=True, nullable=False)
    permission_desc = Column(String(124), nullable=False)
    role_id = Column(String(50), ForeignKey('roles.id'), nullable=False)
    assigned_user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    access_level = Column(Integer, nullable=False, default=0)

    def __init__(self, permission_name, role_id, assigned_user_id, permission_desc="", access_level=0):
        """
        Initialize a Permission instance.

        Args:
            permission_name (str): The name of the permission.
            role_id (str): The ID of the role associated with the permission.
            assigned_user_id (str): The ID of the user to whom the permission is assigned.
            permission_desc (str, optional): The description of the permission.
            access_level (int, optional): The access level of the permission.
        """
        super().__init__()
        self.permission_name = permission_name
        self.role_id = role_id
        self.assigned_user_id = assigned_user_id
        self.permission_desc = permission_desc
        self.access_level = 0
