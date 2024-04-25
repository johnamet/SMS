#!/usr/bin/python3

"""
The script defines the Gradebook class, representing a Gradebook entry.
"""

from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String
from sqlalchemy.orm import relationship, validates

from models.basemodel import BaseModel, Base


class Grade(BaseModel, Base):
    """
    The Gradebook class represents a Gradebook entry.

    Attributes:
        grade (int): The grade of the gradebook entry.
        out_of (int): The total grade or expected grade.
        course_id (int): The ID of the course associated with the gradebook entry.
        class_id (int): The ID of the class associated with the gradebook entry.
        student_id (int): The ID of the student associated with the gradebook entry.
        term (str): The academic term the gradebook entry belongs to.
        grade_desc (str): The description of the gradebook entry.
    """

    __tablename__ = 'gradebook'

    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'),
                   nullable=False, )
    out_of = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100 AND grade <= out_of'),
                    nullable=False, )
    grade_desc = Column(String(50), nullable=True)
    term = Column(String(50), nullable=True)
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

    @validates("grade_desc")
    def validate_grade_desc(self, key, grade_desc):
        desc = ["homework", "classwork", "classtest",
                "assessment", "exam", "dictation", "quiz"]
        if not grade_desc.lower() in desc:
            raise ValueError(f"Grade description must be either {desc}")

    def __init__(self, grade,
                 grade_desc,
                 term,
                 course_id, class_id, student_id,
                 out_of=10,
                 *args, **kwargs):
        """
        Initialize a Gradebook instance.

        Args:
            grade (int): The grade of the gradebook entry.
            out_of (int): The total grade or expected grade.
            grade_desc (str): The description of the gradebook entry. e.g. homework, classwork, etc.
            term (str): The academic term the gradebook entry belongs to e.g. term 1, term 2, first semester.
            course_id (str): The ID of the course associated with the gradebook entry.
            class_id (str): The ID of the class associated with the gradebook entry.
            student_id (str): The ID of the student associated with the gradebook entry.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.grade = grade
        self.grade_desc = grade_desc
        self.term = term
        self.course_id = course_id
        self.class_id = class_id
        self.student_id = student_id
        self.out_of = out_of
