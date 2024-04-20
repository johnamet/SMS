#!/usr/bin/python3

"""
The script defines the class model
"""
from sqlalchemy import String, Column, ForeignKey

from models.basemodel import BaseModel, Base


class Class(BaseModel, Base):
    """
    The class model
    """
    __tablename__ = 'classes'
    class_name = Column(String, nullable=False)
    head_class_teacher = Column(String, ForeignKey("staff.id"), nullable=False)
    academic_year = Column(String, nullable=False)
    assist_class_teacher = Column(String, ForeignKey("staff.id"), nullable=True)

    def __init__(self, class_name,
                 head_class_teacher,
                 academic_year,
                 assist_class_teacher=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.class_name = class_name
        self.head_class_teacher = head_class_teacher
        self.academic_year = academic_year
        self.assist_class_teacher = assist_class_teacher
