#!/usr/bin/python3
"""
Test module for user management module
"""
import unittest

from models import User
from modules.user_management.user_management import UserManagement


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.user_management = UserManagement()
        # Consider using a test database or in-memory storage for testing

    def test_create_user_valid_data(self):
        # Valid user data
        user_data = {
            "email": "test1234@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        # Create user
        user, msg = self.user_management.create_user(user_data)
        self.assertIsNotNone(user)  # Check user object is created
        self.assertTrue(user.email == user_data["email"])  # Verify email

    def test_create_user_duplicate_email(self):
        # Existing user data
        user_data = {
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        # Create user (should fail)
        with self.assertRaises(Exception) as e:  # Expect an exception
            self.user_management.create_user(user_data)
        self.assertEqual(str(e.exception), "Email already exists")  # Verify error message

    def test_create_user_invalid_data(self):
        # Missing mandatory field
        invalid_data = {
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe"
        }

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.create_user(invalid_data)
        self.assertIn("Email cannot be empty", str(e.exception))  # Verify error message

    def test_create_user_invalid_email(self):
        # Invalid email format
        invalid_email = "invalid_email"

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.create_user({
                "email": invalid_email,
                "password": "StrongPassword123!",
                "first_name": "John",
                "last_name": "Doe",
                "gender": 'Male'
            })
        self.assertIn("Invalid email format", str(e.exception))  # Verify error message

    def test_read_user_existing(self):
        # Existing user data (created in a previous test)
        user_data = {
            "email": "testtest@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        user = User(**user_data)

        user.save()

        # Read user
        user, msg = self.user_management.get_user(user.id)
        self.assertIsNotNone(user)  # Check user object retrieved
        self.assertEqual(user.email, user_data["email"])  # Verify email

    def test_read_user_nonexistent(self):
        # Non-existent user id
        nonexistent_id = "24edfdhgj12reimdgk"

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.get_user(nonexistent_id)
        self.assertEqual(str(e.exception), "User not found")  # Verify error message

    def test_update_user_valid_data(self):
        # Existing user data (created in a previous test)
        user_data = {
            "email": "johnnyjohnny@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }
        user = User(**user_data)
        user.save()

        # Update data
        update_data = {"contact_number": "+1234567890"}

        # Update user
        updated_user, msg = self.user_management.update_user(user.id, **update_data)
        self.assertEqual(updated_user.contact_number, update_data["contact_number"])  # Verify update

    def test_update_user_invalid_data(self):
        # Existing user data (created in a previous test)
        user_data = {
            "email": "testjohnny@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        user = User(**user_data)
        user.save()

        # Invalid update data (e.g., empty string for phone number)
        invalid_update_data = {"contact_number": ""}

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.update_user(user.id, **invalid_update_data)
        self.assertIn("Invalid update data", str(e.exception))  # Verify error message

    def test_update_user_nonexistent(self):
        # Non-existent user id
        nonexistent_id = "213456786789"
        update_data = {"phone_number": "+1234567890"}

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.update_user(nonexistent_id, **update_data)
        self.assertEqual(str(e.exception), "User not found")  # Verify error message

    def test_delete_user_existing(self):
        # Existing user data (created in a previous test)
        user_data = {
            "email": "test123345@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        user = User(**user_data)
        user.save()

        # Delete user
        self.user_management.delete_user(user.id)

        # Attempt to read the deleted user (should raise an exception)
        with self.assertRaises(Exception) as e:
            self.user_management.get_user(user.id)
        self.assertEqual(str(e.exception), "User not found")  # Verify user deleted

    def test_delete_user_nonexistent(self):
        # Non-existent user id
        nonexistent_email = "123rfgbhnki90-09"

        # Expect an exception
        with self.assertRaises(Exception) as e:
            self.user_management.delete_user(nonexistent_email)
        self.assertEqual(str(e.exception), "User not found")  # Verify error message

    # Password Management Test Cases
    # def test_reset_password_valid_email(self):
    #     # Existing user data (created in a previous test)
    #     user_data = {
    #         "email": "test@example.com",
    #         "password": "StrongPassword123!",
    #         "first_name": "John",
    #         "last_name": "Doe"
    #     }
    #     user = self.user_management.create_user(**user_data)
    #
    #     # Reset password
    #     self.user_management.reset_password(user.email)
    #
    #     # Password reset functionality implementation specific (check reset email sent)
    #     # You might need to mock email sending functionality for testing

    # def test_reset_password_nonexistent_email(self):
    #     # Non-existent user email
    #     nonexistent_email = "nonexistent@example.com"
    #
    #     # Expect an exception
    #     with self.assertRaises(Exception) as e:
    #         self.user_management.reset_password(nonexistent_email)
    #     self.assertEqual(str(e.exception), "User not found")  # Verify error message

    def test_change_password_valid_data(self):
        # Existing user data (created in a previous test)
        user_data = {
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        user = User(**user_data)

        user.save()
        # New password data
        new_password_data = {
            "current_password": user_data["password"],
            "new_password": "NewStrongPassword!12"
        }

        # Change password
        self.user_management.change_password(user.id, new_password_data["new_password"])

        # Password update functionality implementation specific
        # You might need to re-authenticate the user or verify the password is changed

    # def test_change_password_incorrect_current(self):
    #     # Existing user data (created in a previous test)
    #     user_data = {
    #         "email": "test@example.com",
    #         "password": "StrongPassword123!",
    #         "first_name": "John",
    #         "last_name": "Doe"
    #     }
    #     user = self.user_management.create_user(user_data)
    #
    #     # Incorrect current password
    #     invalid_data = {
    #         "current_password": "WrongPassword",
    #         "new_password": "NewStrongPassword!"
    #     }

    # Expect an exception
    # with self.assertRaises(Exception) as e:
    #     self.user_management.change_password(user.email, invalid_data)
    # self.assertEqual(str(e.exception), "Invalid current password")  # Verify error message

    # def test_change_password_weak_password(self):
    #     # Existing user data (created in a previous test)
    #     user_data = {
    #         "email": "test@example.com",
    #         "password": "StrongPassword123!",
    #         "first_name": "John",
    #         "last_name": "Doe"
    #     }
    #     user = self.user_management.create_user(user_data)
    #
    #     # New password not meeting complexity requirements
    #     weak_password_data = {
    #         "current_password": user_data["password"],
    #         "new_password": "weakpassword"
    #     }
    #
    #     # Expect an exception
    #     with self.assertRaises(Exception) as e:
    #         self.user_management.change_password(user.email, weak_password_data)
    #     self.assertIn("Password does not meet complexity requirements", str(e.exception))  # Verify error message

    # Security Test Cases
    def test_password_hashing(self):
        # Create a user
        user_data = {
            "email": "test1234567@example.com",
            "password": "StrongPassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }
        user = User(**user_data)
        user.save()

        fetched_user, msg = self.user_management.get_user(user.id)

        # Check password is not stored in plain text
        self.assertNotEqual(fetched_user.password, user_data["password"])  # Verify password not plain text

    # def test_input_validation_email(self):
    #     # Invalid email format
    #     invalid_email = "invalid_email"
    #
    #     # Expect an exception on user creation
    #     with self.assertRaises(Exception) as e:
    #         self.user_management.create_user(**{
    #             "email": invalid_email,
    #             "password": "StrongPassword123!",
    #             "first_name": "John",
    #             "last_name": "Doe"
    #         })
    #     self.assertIn("Invalid email format", str(e.exception))  # Verify error message

    def test_input_validation_password_complexity(self):
        # Password not meeting complexity requirements
        weak_password = "weakpassword"
        user_data = {
            "email": "test@example.com",
            "password": weak_password,
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male"
        }

        # Expect an exception on user creation
        with self.assertRaises(Exception) as e:
            self.user_management.create_user(user_data)
        self.assertIn("Password does not meet complexity requirements.", str(e.exception))  # Verify error message


if __name__ == "__main__":
    unittest.main()
