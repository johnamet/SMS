#!/usr/bin/python3
"""
Parent model
"""

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel

# Import Base.metadata here
from models.basemodel import Base

parent_student_association = Table('parent_student_association', Base.metadata,
                                   Column("parent_id", String(50), ForeignKey('parents.id'), nullable=False),
                                   Column("student_id", String(50), ForeignKey('students.id'), nullable=False))


class Parent(BaseModel, Base):
    """
    The Parent model represents a parent entity.

    Attributes:
        id (str): The ID of the parent.
        marital_status (str): The marital status of the parent.
        occupation (str): The occupation of the parent.
        partner (str): The name of the other parent.
        rel_child (str): The relationship between the parent and the child e.g. Aunty, Mother etc.
        students (relationship): Relationship attribute to access the children associated with the parent.
    """

    __tablename__ = 'parents'

    id = Column(String(50), ForeignKey("users.id"), primary_key=True)
    marital_status = Column(String(50))  # Limiting to 50 characters
    occupation = Column(String(124))  # Limiting to 124 characters
    rel_child = Column(String(50))
    partner = Column(String(50))
    students = relationship("Student", secondary=parent_student_association, back_populates="parents")

    def __init__(self, parent_id, marital_status=None, occupation=None, **kwargs):
        """
        Initialize a Parent instance.

        Args:
            parent_id (str): The ID of the parent.
            marital_status (str): The marital status of the parent.
            occupation (str): The occupation of the parent.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.id = parent_id
        self.marital_status = marital_status
        self.occupation = occupation
