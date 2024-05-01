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

    def __init__(self, student_id=None, class_id=None, academic_year=None, term=None):
        """
        Initializes the GradebookManagement instance.
        """
        self.student_id = student_id
        self.class_id = class_id
        self.academic_year = academic_year
        self.term = term

    def _get_gradebook_query(self):
        """
        Builds a SQLAlchemy query based on student_id or class_id.

        Returns:
            SQLAlchemy query object: The query for retrieving gradebooks.
        """
        query = storage.query(Grade)
        if self.student_id:
            query = query.filter(Grade.student_id == self.student_id)

        if self.class_id:
            query = query.filter(Grade.class_id == self.class_id)

        if self.academic_year:
            query = query.filter(Grade.academic_year == self.academic_year)

        if self.term:
            query = query.filter(Grade.term == self.term)

        return query

    def _execute_query(self, query):
        """
        Executes the provided query and returns the results or error message.

        Args:
            query (SQLAlchemy query object): The query to execute.

        Returns:
            tuple: A tuple containing the retrieved data or error message,
                   and a success/failure status.
        """
        try:
            if isinstance(query, Grade):
                return query, "Retrieved gradebook successfully."
            else:
                results = query.all()
                return results, "Retrieved gradebook successfully."
        except Exception as e:
            return None, f"Failed to retrieve gradebook: {e}"

    def get_gradebooks(self):
        """
        Retrieves gradebooks based on student_id or class_id.

        Returns:
            tuple: A tuple containing the retrieved gradebooks or error message,
                   and a success/failure status.
        """
        query = self._get_gradebook_query()
        return self._execute_query(query)

    def get_gradebook_by_id(self, grade_id):
        """
        Retrieve a gradebook by its ID.

        Args:
            grade_id (str): The ID of the gradebook to retrieve.

        Returns:
            tuple: A tuple containing the retrieved gradebook or error message,
                   and a success/failure status.
        """
        return self._execute_query(storage.query(Grade).get(grade_id))

    def record_a_grade(self, grade_data):
        """
        Create a new grade in the database.

        Args:
            grade_data (dict): A dictionary containing grade information.

        Returns:
            tuple: A tuple containing the created grade object or error message,
                   and a success/failure status.
        """
        try:
            if self.student_id and "student_id" not in grade_data:
                grade_data["student_id"] = self.student_id
            if self.class_id and "class_id" not in grade_data:
                grade_data["class_id"] = self.class_id
            if self.academic_year and "academic_year" not in grade_data:
                grade_data["academic_year"] = self.academic_year
            if self.term and "term" not in grade_data:
                grade_data["term"] = self.term

            gradebook = Grade(**grade_data)
            gradebook.save()
            return gradebook, "Saved grade successfully."
        except Exception as e:
            return None, f"Failed to create gradebook: {e}"

    def update_grade(self, grade_id, **kwargs):
        """
        Update information of a gradebook.

        Args:
            grade_id (str): The ID of the gradebook to update.
            **kwargs: Additional keyword arguments for updating gradebook attributes.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        gradebook = storage.get_by_id(Grade, grade_id)
        if gradebook:
            gradebook.update(**kwargs)
            gradebook.save()
            return True, "Successfully updated gradebook."
        else:
            return False, "Gradebook not found."
        # try:
        #
        # except Exception as e:
        #     return False, f"Failed to update gradebook: {e}"

    def delete_grade(self, grade_id):
        """
        Delete a gradebook by its ID.

        Args:
            grade_id (str): The ID of the grade to delete.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        if storage.get_by_id(Grade, grade_id):
            storage.delete_by_id(Grade, grade_id)
            if not storage.get_by_id(Grade, grade_id):
                return True, "Gradebook deleted successfully."
            else:
                return False, f"Failed to delete gradebook"
        else:
            return False, "Gradebook not found."
