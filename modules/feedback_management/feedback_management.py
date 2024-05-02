#!/usr/bin/python3
"""
This module provides functionality for managing feedback.
"""

from models import storage
from models.feedback import Feedback


class FeedbackManagement:
    """
    FeedbackManagement class provides methods for managing feedback.
    """

    def create_feedback(self, feedback):
        """
        Create a new feedback.

        Args:
            feedback (Feedback): The feedback object to be created.
        """
        try:
            storage.new(feedback)
            storage.save()
            return True, "Feedback created successfully."
        except Exception as e:
            return False, f"Failed to create feedback: {str(e)}"

    def get_feedback_by_id(self, feedback_id):
        """
        Retrieve feedback by its ID.

        Args:
            feedback_id (str): The ID of the feedback.

        Returns:
            Feedback: The feedback object if found, None otherwise.
        """
        try:
            return storage.get(Feedback, feedback_id)
        except Exception as e:
            print(f"Error retrieving feedback by ID: {str(e)}")
            return None

    def get_feedback_by_user(self, user_id):
        """
        Retrieve feedback given by a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of feedback objects given by the user.
        """
        try:
            all_feedback = storage.all(Feedback)
            return [feedback for feedback in all_feedback.values() if feedback.user_id == user_id]
        except Exception as e:
            print(f"Error retrieving feedback by user: {str(e)}")
            return []

    def delete_feedback(self, feedback_id):
        """
        Delete feedback by its ID.

        Args:
            feedback_id (str): The ID of the feedback to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            feedback = storage.get(Feedback, feedback_id)
            if feedback:
                storage.delete(feedback)
                storage.save()
                return True, "Feedback deleted successfully."
            else:
                return False, "Feedback not found."
        except Exception as e:
            return False, f"Failed to delete feedback: {str(e)}"
