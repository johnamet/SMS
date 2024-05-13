#!/usr/bin/python3

"""
Class Management Module

This module provides functionality for managing classes in the school system,
including marking attendance, retrieving class information, enrolling and
unenrolling students, and more.
"""

from flask import jsonify, request, abort, make_response

from models import storage, Student
from modules.class_management.class_management import ClassManagement
from modules.service.v1.microservices import services
from modules.user_management.user_management import UserManagement

class_management = ClassManagement()
user_management = UserManagement()


@services.route('/classes', methods=['GET'], strict_slashes=False)
def get_all_classes():
    """
    Retrieves information about all classes.

    Returns:
        JSON: Information about all classes.
    """
    try:
        classes, msg = class_management.get_classes()
        class_list = []
        for class_ in classes:
            class_details = class_.serialize()

            class_details["grades"] = [grade.serialize() for grade in class_.gradebooks]
            class_details["attendances"] = []

            class_details["students"] = [student.serialize() for student in class_.students]
            teacher, _ = user_management.get_user(class_.head_class_teacher)
            class_details['class_teacher'] = teacher.first_name + " " + teacher.last_name
            if class_.assist_class_teacher:
                assist, _ = user_management.get_user(class_.assist_class_teacher)
                class_details['assist_class_teacher'] = assist.first_name + " " + assist.last_name

            for attendance in class_.attendances:
                student_name = attendance.student.first_name + " " + attendance.student.last_name
                attendance = attendance.serialize()
                attendance['student_name'] = student_name

                class_details['attendances'].append(attendance)

            class_list.append(class_details)

        result = {
            "status_msg": msg,
            "classes": class_list
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


@services.route("/students/<student_id>", methods=["GET"], strict_slashes=False)
def get_student(student_id):
    student = storage.get_by_id(Student, student_id)

    result = {
        "student": student.serialize(),
        "message": "Student Retrieved Successfully"
    }

    return jsonify(result), 200
