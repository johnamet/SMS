#!/usr/bin/python3
"""
The user management module
"""
from models import storage, User


class UserManagement:
    def create_user(self, first_name, last_name, email, password, **kwargs):
        # Check if a user with the given email already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            return None, "User with this email already exists"

        # Create a new user
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password, **kwargs)
        storage.new(user)
        return user, "User created successfully"

    def update_user(self, user_id, **kwargs):
        # Retrieve the user by ID
        user = storage.get_by_id(User, user_id)
        if not user:
            return None, "User not found"

        # delete existing record in database to avoid conflict
        storage.delete(user)

        user.update(**kwargs)
        storage.save(user)

        return user, "User updated successfully"

    def delete_user(self, user_id):
        # Retrieve the user by ID
        user = storage.get_by_id(user_id)
        if not user:
            return False, "User not found"

        # Delete the user
        user.delete()
        return True, "User deleted successfully"
