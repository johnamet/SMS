#!/usr/bin/python3

"""
The script defines the class model
"""
from models.basemodel import BaseModel


class Class(BaseModel):
    """
    The class model
    """

    def __init__(self, class_name,
                 head_class_teacher,
                 academic_year,
                 assist_class_teacher=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.class_name = class_name
        self.head_class_teacher = head_class_teacher
        self.academic_year = academic_year
        self.assist_class_teacher = assist_class_teacher
