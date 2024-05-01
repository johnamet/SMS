#!/usr/bin/python3
"""
Gradebook management service module.

This module provides a RESTful API for managing gradebooks in the school system.
"""
from collections import defaultdict

from flask import jsonify, request, abort

from modules.gradebook_management.gradebook_management import GradebookManagement
from modules.service.v1.microservices import services

gradebook_management = GradebookManagement()


@services.route('/gradebooks', methods=['GET'], strict_slashes=False)
def get_gradebooks():
    """
    Retrieves gradebooks based on student ID or class ID provided in the query parameters.

    Returns:
        JSON (200): A list of retrieved gradebooks and a success message.
        JSON (400): Error message for bad request (e.g., invalid query parameters).
    """
    response = request.get_json()
    student_id = response.get('student_id')
    class_id = response.get('class_id')
    academic_year = response.get('academic_year')
    term = response.get('term')

    gradebook_management.student_id = student_id
    gradebook_management.class_id = class_id
    gradebook_management.academic_year = academic_year
    gradebook_management.term = term

    results, msg = gradebook_management.get_gradebooks()

    results = [gradebook.serialize() for gradebook in results]

    if results is None:
        return abort(400, msg)
    return jsonify({"gradebooks": results, "message": msg}), 200


@services.route('/gradebooks/<grade_id>', methods=['GET'], strict_slashes=False)
def get_gradebook_by_id(grade_id):
    """
    Retrieves a gradebook by its ID.

    Args:
        grade_id (str): The ID of the gradebook to retrieve.

    Returns:
        JSON (200): Retrieved gradebook details and a success message.
        JSON (404): Error message for gradebook not found.
    """
    results, msg = gradebook_management.get_gradebook_by_id(grade_id)
    if results is None:
        return abort(404, msg)
    return jsonify({"gradebook": results, "message": msg}), 200


@services.route('/gradebooks', methods=['POST'], strict_slashes=False)
def record_grade():
    """
    Creates a new gradebook entry.

    Expects data in JSON format containing details like student_id, class_id,
    subject, score, etc.

    Returns:
        JSON (200): The created gradebook object and a success message.
        JSON (400): Error message for bad request (e.g., missing data).
    """
    grade_data = request.get_json()
    if grade_data is None:
        return abort(400, "No data provided in request body.")

    results, msg = gradebook_management.record_a_grade(grade_data)
    if results is None:
        return abort(400, msg)
    return jsonify({"gradebook": results, "message": msg}), 200


@services.route('/gradebooks/<grade_id>', methods=['PUT'], strict_slashes=False)
def update_grade(grade_id):
    """
    Updates information of a gradebook.

    Expects data in JSON format with fields for update (e.g., score, comment).

    Args:
        grade_id (str): The ID of the gradebook to update.

    Returns:
        JSON (200): Success message upon successful update.
        JSON (404): Error message for gradebook not found.
    """
    update_data = request.get_json()
    if update_data is None:
        return abort(400, "No data provided in request body.")

    success, msg = gradebook_management.update_grade(grade_id, **update_data)
    if not success:
        return abort(404, msg)
    return jsonify({"message": msg}), 200


@services.route('/gradebooks/<grade_id>', methods=['DELETE'], strict_slashes=False)
def delete_grade(grade_id):
    """
    Deletes a gradebook by its ID.

    Args:
        grade_id (str): The ID of the gradebook to delete.

    Returns:
        JSON (200): Success message upon successful deletion.
        JSON (404): Error message for gradebook not found.
    """
    success, msg = gradebook_management.delete_grade(grade_id)
    if not success:
        return abort(404, msg)
    return jsonify({"message": msg}), 200
