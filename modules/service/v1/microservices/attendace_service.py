#!/usr/bin/python3
"""
This module provides functionality for attendance tracking.
"""

from flask import jsonify, request, abort, make_response

from models import Attendance
from modules.attendance_tracking.attendance_management import AttendanceManagement
from modules.service.v1.microservices import services

attendance_management = AttendanceManagement()


@services.route('/attendance', methods=['GET'], strict_slashes=False)
def get_all_attendance():
    """
    Retrieves attendance records for all students.

    Returns:
        JSON: Attendance records for all students.
    """
    try:
        attendances, msg = attendance_management.get_attendance()
        attendance_dict = {attendance.id: attendance.serialize()
                           for attendance in attendances}
        result = {
            "status_msg": msg,
            "attendances": attendance_dict
        }
        return make_response(jsonify(result), 200)
    except Exception as e:
        abort(500)


@services.route("/attendance/<attendance_id>", methods=["GET"], strict_slashes=False)
def get_attendance(attendance_id):
    """
    Retrieves attendance for a specific attendance record.

    Args:
        attendance_id (str): ID of the attendance record.

    Returns:
        JSON: Attendance record for the specified ID.
    """
    try:
        if not attendance_id:
            abort(400, "Attendance ID cannot be empty")

        attendance, msg = attendance_management.get_attendance(id=attendance_id)
        if attendance:
            attendance = attendance[0]
        else:
            abort(404, "Attendance record not found")

        return jsonify({attendance_id: attendance.serialize(), "status_msg": msg}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, )


@services.route("/attendance/academic_year/<academic_year>/term/<term>")
def get_attendance_by_term_academic_year(academic_year, term):
    """
    Retrieves attendance for a sepcific academic year and term

    Args:
        academic_year (str): Academic year.
        term (str): Term.

    Returns:
        JSON: Attendance records for the specified academic year and term.
    """
    try:
        if not academic_year:
            abort(400, "Academic year cannot be empty")
        if not term:
            abort(400, "Term cannot be empty")

        term = term.replace("_", " ")
        academic_year = academic_year.replace("_", "/")

        attendance_management.term = term
        attendance_management.academic_year = academic_year
        attendances, msg = attendance_management.get_attendance()

        # for attendance in attendances:
        #     if attendance.classe.class_name in attendance_dict:
        #         if attendance.date.strftime("%A, %d-%m-%y") in attendance_dict[attendance.classe.class_name]:
        #             (attendance_dict[attendance.classe.class_name][attendance.date.strftime("%A, %d-%m-%y")]
        #              .serviceend(attendance.serialize()))
        #         else:
        #             attendance_dict[attendance.classe.class_name] \
        #                 [attendance.date.strftime("%A, %d-%m-%y")] = [attendance.serialize()]
        #     else:
        #         attendance_dict[attendance.classe.class_name] \
        #             [attendance.date.strftime("%A, %d-%m-%y")] = [attendance.serialize()]

        attendance_dict = {attendance.id: attendance.serialize() for attendance in attendances}

        result = {
            "academic_year": academic_year,
            "term": term,
            "attendances": attendance_dict
        }

        return jsonify(result), 200

    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


@services.route("/attendance/student/<student_id>", methods=["GET"], strict_slashes=False)
def get_attendance_student(student_id):
    """
    Retrieves attendance for a specific student.

    Args:
        student_id (str): ID of the student.

    Returns:
        JSON: Attendance records for the specified student.
    """
    try:
        if not student_id:
            abort(400, "Student ID cannot be empty")

        attendances, msg = attendance_management.get_student_attendance(student_id)
        # attendance_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict())))
        # # for attendance in attendances:
        #     class_name = attendance.classe.class_name
        #     academic_year = attendance.academic_year
        #     date = attendance.date.strftime("%A, %d-%m-%Y")
        #     term = attendance.term
        #     attendance_dict[class_name][academic_year][term][date] = attendance.serialize()

        # Convert to normal dict
        attendance_dict = {attendance.id: attendance.serialize() for attendance in attendances}

        result = {
            "student_name": attendances[0].student.first_name + " " + attendances[0].student.last_name,
            "result": attendance_dict,
        }

        return jsonify(result), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route("/attendance/class/<class_id>", methods=["GET"], strict_slashes=False)
def get_attendance_by_class(class_id):
    """
    Retrieves attendance for a specific class.

    Args:
        class_id (str): ID of the class.

    Returns:
        JSON: Attendance records for the specified class.
    """
    try:
        if not class_id:
            abort(400, "Student ID cannot be empty")

        attendances, msg = attendance_management.get_attendance_by_class_id(class_id=class_id)
        # Initialize an empty nested dictionary to store attendance data
        # attendance_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
        # for attendance in attendances:
        #     academic_year = attendance.academic_year
        #     term = attendance.term
        #     date_str = attendance.date.strftime("%A, %d-%m-%Y")
        #     student_name = f"{attendance.student.first_name} {attendance.student.last_name}"
        #
        #     # Use defaultdict to handle nested dictionaries
        #     attendance_dict[academic_year][term][date_str][student_name].serviceend(attendance)
        #
        # # Convert defaultdict to regular dictionary
        # attendance_dict = dict(attendance_dict)

        attendance_dict = {attendance.id: attendance.serialize() for attendance in attendances}
        result = {
            "class_id": class_id,
            "class_name": attendances[0].classe.class_name,
            "attendance": attendance_dict
        }
        # for attendance in attendances:
        #     acd_year = attendance.academic_year
        #     term = attendance.term
        #     date_ = attendance.date.stftime("%A, %d-%m-%y")
        #     student = f"{attendance.student.first_name} {attendance.student.last_name}"
        #
        #     if acd_year in attendance_dict:
        #         if term in attendance_dict[acd_year]:
        #             if date_ in attendance_dict[acd_year][term]:
        #                 if student in attendance_dict[acd_year][term][date_]:
        #                     attendance_dict[acd_year][term][date_][student].serviceend(attendance)
        #                 else:
        #                     attendance_dict[acd_year][term][date_][student] = [attendance]
        #             else:
        #                 attendance_dict[acd_year][term][date_][student] = [attendance]
        #         else:
        #             attendance_dict[acd_year][term][date_][student] = [attendance]
        #     else:
        #         attendance_dict[acd_year][term][date_][student] = [attendance]

        return jsonify(result), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route('/attendance', methods=['POST'], strict_slashes=False)
def create_attendance():
    """
    Creates a new attendance record.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        student_id = data.get('student_id')
        class_id = data.get('class_id')
        status = data.get('status')
        term = data.get('term')
        academic_year = data.get('academic_year')

        if not student_id or not status:
            abort(400, "Student ID and status are required")

        if not term and not academic_year:
            abort(400, "Term and academic_year are required")

        attendance_management.term = term
        attendance_management.academic_year = academic_year
        attendance_management.class_id = class_id

        attendance, msg = attendance_management.create_attendance(student_id, status)

        return jsonify({"message": "Attendance record created successfully", "attendance_id": attendance.id}), 201
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route('/attendance/mark', methods=['POST'], strict_slashes=False)
def mark_attendance():
    """
    Marks attendance for multiple students.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        attendances = data.get('attendances')
        if not attendances:
            abort(400, "Attendances list is required")

        # convert dict to Attendance obj
        attendances = [Attendance(**attendance) for attendance in attendances]

        success, message = attendance_management.mark_attendance(attendances)

        if success:
            return jsonify({"message": message}), 200
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@services.route('/attendance/<attendance_id>', methods=['PUT'], strict_slashes=False)
def update_attendance(attendance_id):
    """
    Updates an existing attendance record.

    Args:
        attendance_id (str): ID of the attendance record.

    Returns:
        JSON: Message indicating success or failure of the operation.
    """
    try:
        if not attendance_id:
            abort(400, "Attendance ID cannot be empty")

        data = request.get_json()
        if not data:
            abort(400, "Request body cannot be empty")

        success, message = attendance_management.update_attendance(attendance_id, **data)

        if success:
            return make_response(jsonify({"message": message}), 200)
        else:
            abort(400, )
    except ValueError as ve:
        abort(400, )
    except Exception as e:
        abort(500)
