#!/usr/bin/python3
"""
Gradebook management module.

This module provides functionality for managing gradebooks in the school system.
"""

from collections import defaultdict
from models import Grade, storage

class GradebookManagement:
    """
    Gradebook management class.

    This class provides functionality for managing gradebooks in the school system.
    """

    def __init__(self, class_id=None, student_id=None):
        """
        Initializes the GradebookManagement instance.
        """
        self.class_id = class_id
        self.student_id = student_id

    def create_gradebook(self, grade):
        """
        Create a new gradebook.

        Args:
            grade (Grade): Gradebook to create.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            gradebook = grade
            gradebook.save()
            return True, "Saved grade successfully."
        except Exception as e:
            return False, f"Failed to create gradebook: {e}"

    def get_gradebook(self, gradebook_id):
        """
        Retrieve a gradebook by its ID.

        Args:
            gradebook_id (int): The ID of the gradebook to retrieve.

        Returns:
            Grade: The gradebook object if found, None otherwise.
        """
        return storage.get(Grade, gradebook_id)

    def update_gradebook(self, gradebook_id, **kwargs):
        """
        Update information of a gradebook.

        Args:
            gradebook_id (int): The ID of the gradebook to update.
            **kwargs: Additional keyword arguments for updating gradebook attributes.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            gradebook = storage.get(Grade, gradebook_id)
            if gradebook:
                gradebook.update(**kwargs)
                gradebook.save()
                return True, "Successfully updated gradebook."
            else:
                return False, "Gradebook not found."
        except Exception as e:
            return False, f"Failed to update gradebook: {e}"

    def _group_gradebooks(self, gradebooks, group_by):
        """
        Group gradebooks by the specified attributes.

        Args:
            gradebooks (list): List of gradebook objects.
            group_by (list): List of attributes to group by.

        Returns:
            dict: A nested dictionary where keys represent the group_by attributes and values are nested dictionaries or lists of gradebook objects.
        """
        grouped_gradebooks = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for gradebook in gradebooks:
            group_by_values = [getattr(gradebook, attr) for attr in group_by[:-1]]
            current_dict = grouped_gradebooks
            for value in group_by_values:
                current_dict = current_dict[value]
            current_dict[group_by[-1]].append(gradebook)

        return grouped_gradebooks

    def get_class_gradebook(self, class_id, group_by=["term", "student", "course", "grade_desc"]):
        """
        Get gradebooks for a specific class grouped by the specified attributes.

        Args:
            class_id (int): The ID of the class.
            group_by (list, optional): List of attributes to group by in the specified order. Defaults to ["term", "student", "course", "grade_desc"].

        Returns:
            dict: A nested dictionary where keys represent the group_by attributes and values are nested dictionaries or lists of gradebook objects.
        """
        try:
            gradebooks = storage.query(Grade).filter(Grade.class_id == class_id).all()
            return self._group_gradebooks(gradebooks, group_by)
        except Exception as e:
            return {}, f"Failed to get class gradebook: {e}"

    def get_student_gradebook(self, student_id, group_by=["classe","term", "course", "grade_desc"]):
        """
        Get gradebooks for a specific student grouped by the specified attributes.

        Args:
            student_id (str): The ID of the student.
            group_by (list, optional): List of attributes to group by in the specified order. Defaults to ["term", "course", "grade_desc"].

        Returns:
            dict: A nested dictionary where keys represent the group_by attributes and values are nested dictionaries or lists of gradebook objects.
        """
        try:
            gradebooks = storage.query(Grade).filter(Grade.student_id == student_id).all()
            return self._group_gradebooks(gradebooks, group_by)
        except Exception as e:
            return {}, f"Failed to get student gradebook: {e}"

    def delete_gradebook(self, gradebook_id):
        """
        Delete a gradebook by its ID.

        Args:
            gradebook_id (int): The ID of the gradebook to delete.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            storage.delete_by_id(Grade, gradebook_id)
            return True, "Gradebook deleted successfully."
        except Exception as e:
            return False, f"Failed to delete gradebook: {e}"
