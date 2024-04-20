#!/usr/bin/python3
"""
This module contains the Feedbacks model
"""
from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Feedbacks(BaseModel, Base):
    """
    Feedbacks model
    Args:
        content (str): The content of the feedbacks
        user_id (int): The user id
    """

    __tablename__ = 'feedbacks'

    content = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    def __init__(self, content, user_id, **kwargs):
        super().__init__(**kwargs)

        self.content = content
        self.user_id = user_id
