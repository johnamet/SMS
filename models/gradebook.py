#!/usr/bin/python3

"""
The script defines the Gradebook class, representing a Gradebook entry.
"""

from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String
from sqlalchemy.orm import relationship, validates

from models.basemodel import BaseModel, Base


class Gradebook(BaseModel, Base):
    """
    The Gradebook class represents a Gradebook entry.

    Attributes:
        grade (int): The grade of the gradebook entry.
        course_id (int): The ID of the course associated with the gradebook entry.
        class_id (int): The ID of the class associated with the gradebook entry.
        student_id (int): The ID of the student associated with the gradebook entry.
    """

    __tablename__ = 'gradebook'

    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'),
                   nullable=False, )
    course_id = Column(String(50), ForeignKey('courses.id'), nullable=False)
    class_id = Column(String(50), ForeignKey('classes.id'), nullable=False)
    student_id = Column(String(50), ForeignKey('students.id'), nullable=False)

    # Define relationships
    course = relationship("Course", back_populates="gradebooks")
    classe = relationship("Class", back_populates="gradebooks")
    student = relationship("Student", back_populates="gradebooks")

    @validates("grade")
    def validate_grade(self, key, grade):
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100")

        return grade

    def __init__(self, grade, course_id, class_id, student_id, *args, **kwargs):
        """
        Initialize a Gradebook instance.

        Args:
            grade (int): The grade of the gradebook entry.
            course_id (str): The ID of the course associated with the gradebook entry.
            class_id (str): The ID of the class associated with the gradebook entry.
            student_id (str): The ID of the student associated with the gradebook entry.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.grade = grade
        self.course_id = course_id
        self.class_id = class_id
        self.student_id = student_id
