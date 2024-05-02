#!/usr/bin/python3

"""
Class Management Module

This module provides functionality for managing classes in the school system,
including marking attendance, retrieving class information, enrolling and
unenrolling students, and more.
"""

from flask import jsonify, request, abort, make_response

from modules.class_management.class_management import ClassManagement
from modules.service.v1.microservices import services

class_management = ClassManagement()


@services.route('/classes', methods=['GET'], strict_slashes=False)
def get_all_classes():
    """
    Retrieves information about all classes.

    Returns:
        JSON: Information about all classes.
    """
    try:
        classes, msg = class_management.get_classes()
        class_dict = {class_.id: class_.serialize() for class_ in classes}
        result = {
            "status_msg": msg,
            "classes": class_dict
        }
        return make_response(jsonify(result), 200)
    except Exception as e:
        abort(500)


@services.route("/classes/<class_id>", methods=["GET"], strict_slashes=False)
def get_class(class_id):
    """
    Retrieves information about a specific class.

    Args:
        class_id (str): ID of the class.

    Returns:
        JSON: Information about the specified class.
    """
    try:
        if not class_id:
            abort(400, "Class ID cannot be empty")

        class_, msg = class_management.get_class_details(class_id)
        if class_:
            return make_response(jsonify({class_id: class_, "status_msg": msg}), 200)
        else:
            abort(404, "Class not found")
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500)


@services.route('/classes', methods=['POST'], strict_slashes=False)
def create_class():
    """
    Creates a new class.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        class_name = data.get('class_name')
        head_class_teacher = data.get('head_class_teacher')
        academic_year = data.get('academic_year')
        courses_list = data.get('courses_list')
        assist_class_teacher = data.get('assist_class_teacher')
        students_list = data.get('students_list')

        if not class_name or not head_class_teacher or not academic_year or not courses_list:
            abort(400, "Class name, head class teacher, academic year, and courses list are required")

        success, message = class_management.create_class(class_name, head_class_teacher, academic_year,
                                                         courses_list, assist_class_teacher, students_list)

        if success:
            return jsonify({"message": message}), 201
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/classes/<class_id>", methods=["PUT"], strict_slashes=False)
def update_class(class_id):
    """
    Updates information about a specific class.

    Args:
        class_id (str): ID of the class.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        if not class_id:
            abort(400, "Class ID cannot be empty")

        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        success, message = class_management.update_class(class_id, **data)

        if success:
            return make_response(jsonify({"message": message}), 200)
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/classes/<class_id>", methods=["DELETE"], strict_slashes=False)
def delete_class(class_id):
    """
    Deletes a specific class.

    Args:
        class_id (str): ID of the class.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        if not class_id:
            abort(400, "Class ID cannot be empty")

        class_management.delete_class(class_id)
        return jsonify({"message": "Class deleted successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")
