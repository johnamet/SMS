#!/usr/bin/python3
"""
Qualification Model
"""

from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Qualification(BaseModel, Base):
    """
    Qualification Model: Represents the qualifications of staff.

    Args:
        name (str): The name of the qualification.
        staff_id (str): The ID of the staff member with the qualification.

    Attributes:
        name (str): The name of the qualification.
        staff_id (str): The ID of the staff member with the qualification.
        desc (str): The description of the qualification.
    """
    __tablename__ = 'qualification'

    name = Column(String(50), nullable=False)
    desc = Column(String(124), nullable=False)
    staff_id = Column(String(50), ForeignKey("staff.id"), nullable=False)

    def __init__(self, name, staff_id, desc, *args, **kwargs):
        """
        Initialize a Qualification instance.

        Args:
            name (str): The name of the qualification.
            staff_id (str): The ID of the staff member with the qualification.
            desc (str): The description of the qualification.

            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.desc = desc
        self.staff_id = staff_id
