#!/usr/bin/python3
"""
Student Model
"""
from models import User


class Student(User):
    """
    Student Model
    """

    __tablename__ = 'students'

    def __init__(self, parent_id,
                 expected_graduation,
                 admission_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_id = parent_id
        self.expected_graduation = expected_graduation
        self.admission_date = admission_date
