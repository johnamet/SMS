#!/usr/bin/python3
"""
This module contains the Announcement model
"""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey

from models.basemodel import BaseModel, Base


class Announcement(BaseModel, Base):
    """
    Announcement model
    Args:
        content (str): The content of the announcement
        staff_id (str): The staff id of the one who made the announcement
        target (str): The target of the announcement
        date (datetime): The date of the announcement
    """

    __tablename__ = 'announcements'

    content = Column(String, nullable=False)
    target = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())
    staff_id = Column(String, ForeignKey("staff.id"), nullable=False)

    def __init__(self, content, staff_id, target, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.content = content
        self.staff_id = staff_id
        self.target = target
        self.date = datetime.now()
