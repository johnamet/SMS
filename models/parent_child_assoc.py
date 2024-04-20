#!/usr/bin/python3
"""
Parent Child Association script
"""
from models.basemodel import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class ParentChildAssociation(Base):
    """
    Parent Child Association table links parent/child relationships
    """
    __tablename__ = 'parent_child_association'
    parent_id = Column(String, ForeignKey('parent.id'), nullable=False)
    student_id = Column(String, ForeignKey('student.id'), nullable=False)
    child = relationship('Student', backref='parents', cascade='all, delete, delete-orphan')
    parent = relationship('Parent', backref='children', cascade='all, delete, delete-orphan')
    extra_data = Column(String(100), nullable=True)