#!/usr/bin/python3
"""
This module contains the Announcement model
"""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, func

from models.basemodel import BaseModel, Base


class Announcement(BaseModel, Base):
    """
    Announcement model representing announcements made by staff members.

    Args:
        content (str): The content of the announcement (max length: 124 characters).
        staff_id (str): The staff ID of the user who made the announcement.
        target (str): The target audience or recipients of the announcement (max length: 50 characters).
        date (datetime): The date and time when the announcement was made.

    Attributes:
        content (str): The content of the announcement.
        target (str): The target audience or recipients of the announcement.
        date (datetime): The date and time when the announcement was made.
        staff_id (str): The staff ID of the user who made the announcement.
    """

    __tablename__ = 'announcements'

    content = Column(String(124), nullable=False)
    target = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    staff_id = Column(String(50), ForeignKey("staff.id"), nullable=False)

    def __init__(self, content, staff_id, target, *args, **kwargs):
        """
        Initialize an Announcement instance.

        Args:
            content (str): The content of the announcement.
            staff_id (str): The staff ID of the user who made the announcement.
            target (str): The target audience or recipients of the announcement.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.content = content[:124]  # Limit content length to 124 characters
        self.staff_id = staff_id.strip()  # Remove leading/trailing whitespaces
        self.target = target.strip()  # Remove leading/trailing whitespaces
        self.date = datetime.now()
