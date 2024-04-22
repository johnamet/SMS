#!/usr/bin/python3
"""
The user model represents a user in the system.
"""

from datetime import datetime

from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.orm import relationship, validates

from models.basemodel import BaseModel, Base


class User(BaseModel, Base):
    """
    The User model represents a user in the system.

    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        other_names (str, optional): The other names of the user.
        contact_number (str, optional): The contact number of the user.
        dob (Date, optional): The date of birth of the user.
        address (str, optional): The address of the user.
        gender (str, optional): The gender of the user.
        last_login_date (Date, optional): The last login date of the user.
        last_login_ip (str, optional): The last login IP address of the user.
        registration_date (Date, optional): The registration date of the user.
        is_active (bool, optional): The status of the user (active/inactive).

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        other_names (str, optional): The other names of the user.
        contact_number (str, optional): The contact number of the user.
        dob (Date, optional): The date of birth of the user.
        address (str, optional): The address of the user.
        gender (str, optional): The gender of the user.
        last_login_date (Date, optional): The last login date of the user.
        last_login_ip (str, optional): The last login IP address of the user.
        registration_date (Date, optional): The registration date of the user.
        is_active (bool): The status of the user (active/inactive).
        feedbacks (relationship): Relationship attribute to access the associated feedbacks.
    """

    __tablename__ = 'users'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    other_names = Column(String(50))
    contact_number = Column(String(50))
    dob = Column(Date)
    gender = Column(String(50), nullable=False)
    address = Column(String(50))
    last_login_date = Column(Date, default=datetime.now)
    last_login_ip = Column(String(50))
    registration_date = Column(Date)
    is_active = Column(Boolean(), default=True)
    feedbacks = relationship("Feedback", backref="user", cascade="all, delete")

    @validates("gender")
    def validate_gender(self, key, gender):
        if gender.lower() not in ["male", "female"]:
            raise ValueError("Gender must be either male or female")
        return gender

    def __init__(self, first_name, last_name, email, password,
                 other_names=None,
                 address=None,
                 last_login_date=datetime.now(),
                 dob=None, last_login_ip=None, *args, **kwargs):
        """
        Initialize a User instance.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            other_names (str, optional): The other names of the user.
            contact_number (str, optional): The contact number of the user.
            address (str, optional): The address of the user.
            dob (Date, optional): The date of birth of the user.
            last_login_ip (str, optional): The last login IP address of the user.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.other_names = other_names
        self.address = address
        self.dob = dob
        self.last_login_date = last_login_date
        self.last_login_ip = last_login_ip
