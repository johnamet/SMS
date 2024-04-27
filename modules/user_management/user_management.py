#!/usr/bin/python3
"""
User Management Module

This module provides functionalities for managing users, including creating, updating, and deleting users,
changing passwords, searching users, and deactivating user accounts.

It includes methods to interact with the database to perform CRUD operations on User, Staff, and Parent entities.
Password validation is also implemented using regular expressions.

Classes:
    UserManagement: Provides methods for managing users.
"""

import re

from models import storage, User, Staff, Parent
from models.user import _hash_password


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


# Example usage:
password = "Password123!"
if validate_password(password):
    print("Password is valid")
else:
    print("Password is not valid")


class UserManagement:
    """
    User Management Class

    This class provides methods for managing users, including creating, updating, and deleting users,
    changing passwords, searching users, and deactivating user accounts.

    Attributes:

    """

    def create_user(self, first_name, last_name, email, password_, **kwargs):
        """
        Create a new user.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.
            password_ (str): The password of the user.
            **kwargs: Additional keyword arguments for user attributes.

        Returns:
            tuple: A tuple containing the created user object and a message.
        """
        existing_user = User.get_by_email(email)
        if existing_user:
            return None, "User with this email already exists"

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password_, **kwargs)
        storage.new(user)
        return user, "User created successfully"

    def update_user(self, user_id, **kwargs):
        """
        Update an existing user.

        Args:
            user_id (str): The ID of the user to update.
            **kwargs: Keyword arguments for user attributes to be updated.

        Returns:
            tuple: A tuple containing the updated user object and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return None, "User not found"

        user.update(**kwargs)
        user.save()

        return user, "User updated successfully"

    def delete_user(self, user_id):
        """
        Delete a user.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return False, "User not found"

        user.delete()
        return True, "User deleted successfully"

    def create_staff(self, user_id, role, **kwargs):
        """
        Create a staff user.

        Args:
            user_id (str): The ID of the user to associate with the staff.
            role (str): The role of the staff user.
            **kwargs: Additional keyword arguments for staff attributes.

        Returns:
            tuple: A tuple containing the created staff object and a message.
        """
        user_ = storage.get_by_id(User, user_id)

        if not user_:
            raise ValueError(f"User with id: {user_id} not found")

        staff = Staff(id=user_id, role=role, **kwargs)
        staff.save()

        return staff, "Staff created successfully"

    def create_parent(self, user_id, **kwargs):
        """
        Create a parent user.
        """

        try:
            parent_user = storage.get_by_id(user_id)

            if not parent_user:
                raise ValueError(f"User with id: {parent_user.id} not found")

            parent = Parent(id=parent_user.id, **kwargs)
            parent.save()
            return parent, "Parent created successfully"
        except ValueError as e:
            return False, f"Failed to create parent: {str(e)}"
        except Exception as e:
            return False, f"Failed to create parent: {str(e)}"

    def delete_staff(self, user_id):
        """
        Delete a staff user.

        Args:
            user_id (str): The ID of the staff user to delete.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            staff = storage.get_by_id(Staff, user_id)

            if not staff:
                raise Exception("Staff not found")
            storage.delete(staff)

            return True, "Staff deleted successfully"
        except ValueError as e:
            return False, f"Deleting Staff unsuccessful {str(e)}"

    def delete_parent(self, parent_id):
        try:
            parent = storage.get_by_id(Parent, parent_id)

            if not parent:
                raise Exception("Parent not found")
            storage.delete(parent)

            return True, "Parent deleted successfully"
        except ValueError as e:
            return False, f"Deleting Parent unsuccessful {str(e)}"

    def get_staff(self, user_id):
        """
        Retrieve a staff user by ID.

        Args:
            user_id (str): The ID of the staff user to retrieve.

        Returns:
            tuple: A tuple containing the retrieved staff object and a message.
        """
        staff = storage.get_by_id(Staff, user_id)

        if not staff:
            return None, "Staff not found"

        return staff, "Staff retrieved successfully"

    def get_user(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            tuple: A tuple containing the retrieved user object and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return None, "User not found"

        return user, "User retrieved successfully"

    def get_staff_role(self, user_id):
        """
        Retrieve the role of a staff user by ID.

        Args:
            user_id (str): The ID of the staff user.

        Returns:
            tuple: A tuple containing the staff role and a message.
        """
        staff = storage.get_by_id(Staff, user_id)
        if not staff:
            return None, "Staff not found"

        return staff.role, "Staff role retrieved successfully"

    def get_parent(self, user_id):
        """
        Retrieve a parent user by ID.

        Args:
            user_id (str): The ID of the parent user to retrieve.

        Returns:
            tuple: A tuple containing the retrieved parent object and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return None, "User not found"

        parent = storage.get_by_id(Parent, user_id)

        if not parent:
            return None, "Parent not found"

        return parent, "Parent retrieved successfully"

    def get_parent_wards(self, user_id):
        """
        Retrieve the children of a parent user by ID.

        Args:
            user_id (str): The ID of the parent user.

        Returns:
            tuple: A tuple containing the retrieved children objects and a message.
        """
        parent = storage.get_by_id(Parent, user_id)

        if not parent:
            return None, "Parent not found"

        return parent.students, "Parent wards retrieved successfully"

    def change_password(self, user_id, current_password, new_password):
        """
        Change the password of a user.

        Args:
            user_id (str): The ID of the user.
            current_password (str): The current password of the user.
            new_password (str): The new password for the user.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return False, "User not found"

        if not user.verify_password(current_password):
            return False, "Current password is incorrect"

        if not validate_password(new_password):
            return False, "New password must be at least 8 characters long and meet complexity requirements"

        user.password = _hash_password(new_password)
        storage.save()
        return True, "Password changed successfully"

    def search_users(self, query):
        """
        Search for users by name, email, or role.

        Args:
            query (str): The search query.

        Returns:
            list: A list of users matching the search query.
        """
        # Implement search logic here
        pass

    def deactivate_user(self, user_id):
        """
        Deactivate a user account.

        Args:
            user_id (str): The ID of the user to deactivate.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = storage.get_by_id(User, user_id)
        if not user:
            return False, "User not found"

        user.is_active = False
        storage.save()
        return True, "User deactivated successfully"

    def get_user_details(self, user_id):
        """
        Get the full details of a user

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            tuple: A tuple containing the full details of the user and a message.
        """

        user = storage.get_by_id(User, user_id)

        if not user:
            return None, "User not found"

        user_details = user.serialize()

        return user_details, "User retrieved successfully"

    def get_staff_details(self, user_id):
        """
        Get the full details of a staff user

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            tuple: A tuple containing the full details of the staff(dict) and a message.
        """

        user = storage.get_by_id(User, user_id)

        if not user:
            return None, "User not found"

        staff = storage.get_by_id(Staff, user_id)

        if not staff:
            return None, "Staff not found"

        user_details = user.serialize()

        user_details.update(staff.serialize())

        return user_details, "Staff retrieved successfully"

    def get_parent_details(self, user_id):
        """
        Get the full details of a parent user

        Args:
            user_id (str): The ID of the parent user.

        Returns:
            tuple: A tuple containing the full details of the parent user and a message.
        """

        user = storage.get_by_id(User, user_id)

        if not user:
            return None, "User not found"

        parent = storage.get_by_id(Parent, user_id)

        if not parent:
            return None, "Parent not found"

        user_details = user.serialize()

        user_details.update(parent.serialize())

        return user_details, "Parent retrieved successfully"

    def get_all_users(self):
        """
        Get all users in the database

        Returns:
            tuple: A tuple containing the users in the database and a message.
        """

        try:
            users = storage.query(User).all()
        except Exception as e:
            return None, f"Unable to retrieve users: {e}"

        return users, "All users retrieved successfully"

    def get_all_staff(self):
        """
        Get all staff users in the database

        Returns:
            tuple: A tuple containing the users in the database and a message.
        """

        try:
            staffs = storage.query(Staff)
            return staffs, "All staff users retrieved successfully"
        except Exception as e:
            return None, f"Unable to retrieve staffs: {e}"

    def get_all_parent(self):
        """
        Get all parent users in the database

        Returns:
            tuple: A tuple containing the users in the database and a message.
        """

        try:
            parents = storage.query(Parent)
            return parents, "All parent users retrieved successfully"
        except Exception as e:
            return None, f"Unable to retrieve parents: {e}"
