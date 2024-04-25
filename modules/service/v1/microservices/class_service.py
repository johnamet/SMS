from flask import jsonify, request, abort, make_response

from modules.service.v1.microservices import services
from modules.course_management.course_management import CourseManagement

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
        course_dict = {course.id: course.serialize() for course in courses}
        result = {
            "status_msg": msg,
            "courses": course_dict
        }
        return make_response(jsonify(result), 200)
    except Exception as e:
        abort(500)


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
            abort(404, "Course not found")
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500)


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


# Endpoint to get courses by teacher
@services.route('/courses/teacher/<teacher_id>', methods=['GET'])
def get_courses_by_teacher(teacher_id):
    courses, message = course_management.get_courses_by_teacher(teacher_id)
    if courses:
        serialized_courses = [course.serialize() for course in courses]
        return jsonify({'courses': serialized_courses, 'message': message}), 200
    else:
        return jsonify({'error': message}), 404


# Endpoint to associate a course with a class
@services.route('/courses/<course_id>/associate_class/<class_id>', methods=['POST'])
def associate_course_with_class(course_id, class_id):
    success, message = course_management.associate_course_with_class(course_id, class_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400
