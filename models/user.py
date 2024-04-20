#!/usr/bin/python3
"""
The user model
"""
from datetime import datetime
from sqlite3 import Date

from sqlalchemy import Column, String, Boolean

from models.basemodel import BaseModel, Base


class User(BaseModel, Base):
    """
    The user model inherits from the base model

    Args:
        first_name: The first name of the user
        last_name: The last name of the user
        email: The email address of the user
        password: The password of the user
        other_names: The other names of the user
        contact_number: The list of contact number of the user
        dob: The date of birth of the user
    """

    __tablename__ = 'users'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    other_names = Column(String(50), nullable=False)
    contact_number = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    address = Column(String(50), nullable=False)
    last_login_date = Column(Date, nullable=False)
    last_login_ip = Column(String(50), nullable=False)
    registration_date = Column(Date, nullable=False)
    is_active = Column(Boolean(), default=True)

    def __init__(self, first_name, last_name, email,
                 password,
                 other_names=None,
                 contact_number=None,
                 address=None,
                 dob=None,
                 last_login_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 last_login_ip=None,
                 *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        if contact_number is None:
            contact_number = []
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.other_names = other_names
        self.contact_number = contact_number
        self.address = address
        self.last_login_date = last_login_date
        self.last_login_ip = last_login_ip
        self.registration_date = None
        self.dob = dob
        self.is_active = False
