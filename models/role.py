#!/usr/bin/python3
"""
Role Model
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel


class Role(BaseModel, Base):
    """
    The Role model represents a role in the system.

    Attributes:
        role_name (str): The name of the role.
        role_desc (str): The description of the role.
        permissions (relationship): Relationship attribute to access associated permissions.
    """

    __tablename__ = "roles"

    role_name = Column(String(50), unique=True, nullable=False)
    role_desc = Column(String(124))

    permissions = relationship("Permission", backref="role")

    def __init__(self, role_name, role_desc="", *args, **kwargs):
        """
        Initialize a Role instance.

        Args:
            role_name (str): The name of the role.
            role_desc (str, optional): The description of the role.
        """
        super().__init__(self, *args, **kwargs)
        self.role_name = role_name
        self.role_desc = role_desc
