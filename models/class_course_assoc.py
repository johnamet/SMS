#!/usr/bin/python3

"""
Class Course Association Table
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models.basemodel import Base


class ClassCourseAssociation(Base):
    """
    Class Course Association Table

    Attributes:
        class_id (str): The ID of the class associated with the course.
        course_id (str): The ID of the course associated with the class.
        description (str): Description of the association.
        course (relationship): Relationship attribute to access the related Course instance.
        classe (relationship): Relationship attribute to access the related Class instance.
    """

    __tablename__ = 'class_course_assoc'
    class_id = Column(ForeignKey('classes.id'), primary_key=True)
    course_id = Column(ForeignKey('courses.id'), primary_key=True)
    description = Column(String(50))
    course = relationship('Course', back_populates="classes")
    classe = relationship('Class', back_populates="courses")
