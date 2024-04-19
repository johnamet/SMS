#!/usr/bin/python3
"""
This module contains the Feedbacks model
"""

from models.basemodel import BaseModel


class Feedbacks(BaseModel):
    """
    Feedbacks model
    Args:
        content (str): The content of the feedbacks
        user_id (int): The user id
    """

    __tablename__ = 'feedbacks'

    def __init__(self, content, user_id, **kwargs):
        super().__init__(**kwargs)

        self.content = content
        self.user_id = user_id
