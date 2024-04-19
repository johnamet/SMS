#!/usr/bin/python3
"""
Parent model
"""
from models.basemodel import BaseModel


class Parent(BaseModel):
    """
    Parent model
    Args:
        id (int): Parent ID
        marital_status (str): Marital status
        occupation (str): Occupation
    """

    __tablename__ = 'parents'

    def __init__(self, id, marital_status=None, occupation=None, **kwargs):
        super().__init__(self, **kwargs)
        self.id = id
        self.marital_status = marital_status
        self.occupation = occupation
