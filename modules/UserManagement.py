#!/usr/bin/python3
"""
The user management module
"""
from models import storage, User


class UserManagement:
    """
    The user management module
    """

    def __init__(self):
        pass

    @staticmethod
    def get_users():
        storage.all(User)