#!/usr/bin/python3

"""
This module defines the Class model, representing a class in the school system.
"""

from models.basemodel import BaseModel
from models.class_course_assoc import ClassCourseAssociation

# !/usr/bin/python3

"""
Class Course Association Table
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models.basemodel import Base


# class ClassCourseAssociation(Base):
#     """
#     Class Course Association Table
#
#     Attributes:
#         class_id (str): The ID of the class associated with the course.
#         course_id (str): The ID of the course associated with the class.
#         description (str): Description of the association.
#         course (relationship): Relationship attribute to access the related Course instance.
#         classe (relationship): Relationship attribute to access the related Class instance.
#     """
#
#     __tablename__ = 'class_course_assoc'
#     class_id = Column(ForeignKey('classes.id'), primary_key=True)
#     course_id = Column(ForeignKey('courses.id'), primary_key=True)
#     description = Column(String(50))
#     course = relationship('Course', back_populates="classes")
#     classe = relationship('Class', back_populates="courses")


class Class(BaseModel, Base):
    """
    The Class model represents a class in the school system.

    Attributes:
        class_name (str): The name of the class.
        head_class_teacher (str): The ID of the head class teacher.
        academic_year (str): The academic year of the class.
        assist_class_teacher (str, optional): The ID of the assistant class teacher (default: None).
        courses (relationship): Relationship attribute to access associated courses.
        attendance (relationship): Relationship attribute to access attendance records.
        gradebooks (relationship): Relationship attribute to access gradebooks.
    """

    __tablename__ = 'classes'
    class_name = Column(String(50), nullable=False)
    head_class_teacher = Column(String(50), ForeignKey("staff.id"), nullable=False)
    academic_year = Column(String(50), nullable=False)
    assist_class_teacher = Column(String(50), ForeignKey("staff.id"))
    courses = relationship(ClassCourseAssociation, back_populates="classe")
    attendances = relationship("Attendance", back_populates="classe", cascade="all, delete-orphan")
    gradebooks = relationship("Gradebook", back_populates="classe")

    def __init__(self, class_name, head_class_teacher,
                 academic_year,
                 assist_class_teacher=None, *args, **kwargs):
        """
        Initialize a Class instance.

        Args:
            class_name (str): The name of the class.
            head_class_teacher (str): The ID of the head class teacher.
            academic_year (str): The academic year of the class.
            assist_class_teacher (str, optional): The ID of the assistant class teacher (default: None).
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(self, *args, **kwargs)
        self.class_name = class_name
        self.head_class_teacher = head_class_teacher
        self.academic_year = academic_year
        self.assist_class_teacher = assist_class_teacher
