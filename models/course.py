#!/usr/bin/python

"""
This module defines the Course model, representing a course offered in the school system.
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models.basemodel import BaseModel, Base
from models.class_course_assoc import ClassCourseAssociation


class Course(BaseModel, Base):
    """
    The Course model represents a course offered in the school system.

    Attributes:
        course_name (str): The name of the course.
        course_description (str): The description of the course.
        teacher_id (str): The ID of the teacher assigned to the course.
        classes (relationship): Relationship attribute to access associated classes.
        gradebooks (relationship): Relationship attribute to access gradebooks.
    """

    __tablename__ = 'courses'
    course_name = Column(String(50), nullable=False)
    course_description = Column(String(124), nullable=False)
    teacher_id = Column(String(50), ForeignKey("staff.id"), nullable=False)
    classes = relationship(ClassCourseAssociation, back_populates="course")
    gradebooks = relationship("Grade", back_populates="course")

    def __init__(self, course_name, course_description, teacher_id, *args, **kwargs):
        """
        Initialize a Course instance.

        Args:
            course_name (str): The name of the course.
            course_description (str): The description of the course.
            teacher_id (str): The ID of the teacher assigned to the course.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(self, *args, **kwargs)
        self.course_name = course_name
        self.course_description = course_description
        self.teacher_id = teacher_id
