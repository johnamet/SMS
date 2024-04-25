#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import Base, BaseModel


class StudentClassAssociation(BaseModel, Base):
    """
    StudentClassAssociation represents the association table between Student and Class models.

    Attributes:
        student_id (str): The ID of the student associated with the class.
        class_id (str): The ID of the class associated with the student.
        student (relationship): Relationship attribute to access the associated Student instance.
        class_ (relationship): Relationship attribute to access the associated Class instance.
    """

    __tablename__ = 'student_class_assoc'

    student_id = Column( ForeignKey("students.id"), primary_key=True)
    class_id = Column(ForeignKey("classes.id"), primary_key=True,)

    student = relationship("Student", back_populates="class_")
    class_ = relationship("Class", back_populates="students")
