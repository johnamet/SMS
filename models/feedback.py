#!/usr/bin/python3
"""
This module contains the Feedbacks model, representing user feedback.
"""

from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Feedback(BaseModel, Base):
    """
    The Feedbacks model represents user feedback.

    Attributes:
        content (str): The content of the feedback.
        user_id (str): The ID of the user providing the feedback.
    """

    __tablename__ = 'feedbacks'

    content = Column(String(255), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    def __init__(self, content, user_id, *args, **kwargs):
        """
        Initialize a Feedbacks instance.

        Args:
            content (str): The content of the feedback.
            user_id (str): The ID of the user providing the feedback.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.content = content
        self.user_id = user_id
