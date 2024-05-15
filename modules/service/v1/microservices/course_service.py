#!/usr/bin/python3

"""
Course Management Microservice

This microservice provides endpoints for managing courses in the school system,
including retrieving, creating, updating, and deleting courses. It also supports
retrieving courses by teacher and class.

Endpoints:
- GET /courses: Retrieves information about all courses.
- GET /courses/<course_id>: Retrieves information about a specific course.
- POST /courses: Creates a new course.
- PUT /courses/<course_id>: Updates information about a specific course.
- DELETE /courses/<course_id>: Deletes a specific course.
- GET /courses/by_teacher/<teacher_id>: Retrieves courses associated with a specific teacher.
- GET /courses/by_class/<class_id>: Retrieves courses associated with a specific class.
"""

from flask import jsonify, request, abort, make_response

from models import storage, User
from modules.course_management.course_management import CourseManagement
from modules.service.v1.microservices import services

course_management = CourseManagement()


@services.route('/courses', methods=['GET'], strict_slashes=False)
def get_all_courses():
    """
    Retrieves information about all courses.

    Returns:
        JSON: Information about all courses.
    """
    try:
        courses, msg = course_management.get_courses()

        course_list = []

        for course in courses:
            classes = course.classes
            teacher = course.teacher
            teacher_ = storage.get_by_id(User, teacher.id)
            course = course.serialize()
            course["classes"] = [class_.classe.serialize() for class_ in classes]
            course["teacher"] = teacher_.first_name + " " + teacher_.last_name
            course_list.append(course)

        result = {
            "status_msg": msg,
            "courses": course_list
        }
        return make_response(jsonify(result), 200)
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/courses/<course_id>", methods=["GET"], strict_slashes=False)
def get_course(course_id):
    """
    Retrieves information about a specific course.

    Args:
        course_id (str): ID of the course.

    Returns:
        JSON: Information about the specified course.
    """
    try:
        if not course_id:
            abort(400, "Course ID cannot be empty")

        course, msg = course_management.get_course_details(course_id)
        if course:
            return jsonify({course_id: course, "status_msg": msg}), 200
        else:
            abort(404, msg)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route('/courses', methods=['POST'], strict_slashes=False)
def create_course():
    """
    Creates a new course.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        if "course_name" not in data:
            abort(400, "Course name cannot be empty")

        if "course_description" not in data:
            abort(400, "Course description cannot be empty")

        if "teacher_id" not in data:
            abort(400, "Teacher ID cannot be empty")

        course, message = course_management.create_course(data)

        if course:
            return jsonify({"course": course.serialize(), "message": message}), 201
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/courses/<course_id>", methods=["PUT"], strict_slashes=False)
def update_course(course_id):
    """
    Updates information about a specific course.

    Args:
        course_id (str): ID of the course.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        if not course_id:
            abort(400, "Course ID cannot be empty")

        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        success, message = course_management.update_course(course_id, **data)

        if success:
            return make_response(jsonify({"message": message}), 200)
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/courses/<course_id>", methods=["DELETE"], strict_slashes=False)
def delete_course(course_id):
    """
    Deletes a specific course.

    Args:
        course_id (str): ID of the course.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        if not course_id:
            abort(400, "Course ID cannot be empty")

        success, message = course_management.delete_course(course_id)
        if success:
            return jsonify({"message": message}), 200
        else:
            abort(404, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/courses/by_teacher/<teacher_id>", methods=["GET"], strict_slashes=False)
def get_course_by_teacher(teacher_id):
    """
    Retrieves courses associated with a specific teacher.

    Args:
        teacher_id (str): ID of the teacher.

    Returns:
        JSON: Courses associated with the specified teacher.
    """
    if teacher_id is None:
        abort(400, "Teacher ID cannot be None")

    try:
        courses, msg = course_management.get_courses_by_teacher(teacher_id)
        if courses or courses == []:
            return jsonify({"courses": {course.id: course.serialize() for course in courses}, "message": msg}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/courses/by_class/<class_id>", methods=["GET"], strict_slashes=False)
def get_course_by_class(class_id):
    """
    Retrieves courses associated with a specific class.

    Args:
        class_id (str): ID of the class.

    Returns:
        JSON: Courses associated with the specified class.
    """
    if class_id is None:
        abort(400, "Class ID cannot be None")

    try:
        courses, msg = course_management.get_courses_by_class(class_id)
        if courses or courses == []:
            return jsonify({"courses": {course.id: course.serialize() for course in courses}, "message": msg}), 200

    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")
