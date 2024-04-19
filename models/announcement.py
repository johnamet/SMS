#!/usr/bin/python3
"""
This module contains the Announcement model
"""
from datetime import datetime

from models.basemodel import BaseModel


class Announcement(BaseModel):
    """
    Announcement model
    Args:
        content (str): The content of the announcement
        staff_id (str): The staff id of the one who made the announcement
        target (str): The target of the announcement
        date (datetime): The date of the announcement
    """

    def __init__(self, content, staff_id, target, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.content = content
        self.staff_id = staff_id
        self.target = target
        self.date = datetime.now()
