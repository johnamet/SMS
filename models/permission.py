#!/usr/bin/python3
"""
The permission classes defined in this module
"""
from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Permission(BaseModel, Base):
    """
    The permission for each role
    Args:
        permission_name: name of the permission
        permission_desc: description of the permission
        role_id: id of the role
    """
    __tablename__ = 'permissions'
    permission_name = Column(String, unique=True, nullable=False)
    permission_desc = Column(String, nullable=False)
    role_id = Column(String, ForeignKey('roles.id'), nullable=False)

    def __init__(self, permission_name, role_id, permission_desc=""):
        super().__init__(self)
        self.permission_name = permission_name
        self.role_id = role_id
        self.permission_desc = permission_desc
