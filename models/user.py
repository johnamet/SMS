#!/usr/bin/python3
"""
The user model
"""
from datetime import datetime

from models.basemodel import BaseModel


class User(BaseModel):
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

    def __init__(self, first_name, last_name, email,
                 password,
                 other_names=None,
                 contact_number=None,
                 address=None,
                 dob=None,
                 *args, **kwargs):
        super().__init__( self, *args, **kwargs)

        if contact_number is None:
            contact_number = []
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.other_names = other_names
        self.contact_number = contact_number
        self.address = address
        self.last_login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registration_date = None
        self.dob = dob