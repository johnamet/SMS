#!/usr/bin/python3
"""
The user model represents a user in the system.
"""

from datetime import datetime
from hashlib import md5
import re
# from email_validator import validate_email

from bcrypt import gensalt
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.orm import relationship, validates

from models.basemodel import BaseModel, Base


def _hash_password(password):
    """
           Hashes the given password using bcrypt.

           Args:
               password (str): The password to hash.

           Returns:
               str: The hashed password.
           """
    salt = gensalt()
    hashed_password = md5(password.encode('utf-8')).hexdigest()
    return hashed_password

def validate_password(password_):
    """
    Validate a password based on the following criteria:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character (!@#$%^&*()-_+=)

    Args:
        password_ (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Check length
    if len(password_) < 8:
        return False

    # Check for uppercase letter
    if not re.search(r"[A-Z]", password_):
        return False

    # Check for lowercase letter
    if not re.search(r"[a-z]", password_):
        return False

    # Check for digit
    if not re.search(r"\d", password_):
        return False

    # Check for special character
    if not re.search(r"[!@#$%^&*()-_+=]", password_):
        return False

    # All criteria met
    return True


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
        permission (Permission, optional): The permission of the user.
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
        permission (Permission, optional): The permission of the user.
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
    password = Column(String(128), nullable=False)
    other_names = Column(String(50))
    contact_number = Column(String(50))
    dob = Column(Date)
    gender = Column(String(50), nullable=False)
    address = Column(String(50))
    last_login_date = Column(Date, default=datetime.now)
    last_login_ip = Column(String(50))
    registration_date = Column(Date)
    is_active = Column(Boolean(), default=True)
    # permission_id = Column(String(50), ForeignKey("permissions.id"), nullable=True)
    # permission = relationship("Permission", back_populates="user")
    feedbacks = relationship("Feedback", backref="user", cascade="all, delete")

    @validates("gender")
    def validate_gender(self, key, gender):
        if gender.lower() not in ["male", "female"]:
            raise ValueError("Gender must be either male or female")
        return gender

    # @validates("email")
    # def validate_email(self, key, email):
    #     """
    #     Validates the email address format using the `email_validator` library.
    #
    #     Args:
    #         key (str): Name of the field being validated (should be "email").
    #         email (str): The email address to validate.
    #
    #     Raises:
    #         ValueError: If the email address is not valid.
    #     """
    #
    #     try:
    #         # Validate email format using email_validator
    #         if not validate_email(email):
    #             raise ValueError(f"Invalid email address format for: {key}")
    #
    #     except (ValueError, AttributeError) as e:
    #         # Handle potential errors like invalid email format or missing `email_validator`
    #         raise ValueError(f"Error validating email address for: {key}. Exception: {e}")
    #
    #     # No exception raised, email is valid
    #     return True

    def __init__(self, first_name, last_name, email, password,
                 gender,
                 contact_number=None,
                 permission_id=None,
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
        self.password = _hash_password(password)
        self.gender = gender
        self.other_names = other_names
        self.contact_number = contact_number
        self.address = address
        self.dob = dob
        self.last_login_date = last_login_date
        self.last_login_ip = last_login_ip
        self.permission_id = permission_id

    @classmethod
    def get_by_email(cls, email):
        """
        get the user email
        """
        from models import storage

        query = storage.get_by_filter(User, User.email == email)

        return query.first()

    # @property
    # def password(self):
    #     return self.password
    #
    # @password.setter
    # def password(self, password):
    #     if validate_password(password_=password):
    #         self.password = _hash_password(password)
    #     else:
    #         raise ValueError("Password does not meet complexity requirements")
    #
