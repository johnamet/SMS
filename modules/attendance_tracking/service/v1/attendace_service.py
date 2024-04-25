#!/usr/bin/python3
"""
This module provides functionality for attendance tracking.
"""
from modules.attendance_tracking.attendance_management import AttendanceManagement
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

attendance_management = AttendanceManagement()


@app.route('/attendance', methods=['GET'], strict_slashes=False)
def get_all_attendance():
    """
    Retrieves attendance records for all students.

    Returns:
        JSON: Attendance records for all students.
    """
    try:
        attendances = attendance_management.get_attendance()
        attendance_dict = {attendance.id: attendance for attendance in attendances}
        return jsonify(attendance_dict), 200
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@app.route("/attendance/<attendance_id>", methods=["GET"], strict_slashes=False)
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

        attendance = attendance_management.get_attendance(id=attendance_id)
        if not attendance:
            abort(404, "Attendance record not found")

        return jsonify({attendance_id: attendance}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@app.route("/attendance/student/<student_id>", methods=["GET"], strict_slashes=False)
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

        attendances = attendance_management.get_student_attendance(student_id)
        attendance_dict = {attendance.id: attendance for attendance in attendances}

        return jsonify(attendance_dict), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@app.route('/attendance', methods=['POST'], strict_slashes=False)
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
        status = data.get('status')

        if not student_id or not status:
            abort(400, "Student ID and status are required")

        attendance = attendance_management.create_attendance(student_id, status)

        return jsonify({"message": "Attendance record created successfully", "attendance": attendance}), 201
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@app.route('/attendance/mark', methods=['POST'], strict_slashes=False)
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

        success, message = attendance_management.mark_attendance(attendances)

        if success:
            return jsonify({"message": message}), 200
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")


@app.route('/attendance/<attendance_id>', methods=['PUT'], strict_slashes=False)
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
            return jsonify({"message": message}), 200
        else:
            abort(400, message)
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, f"Internal Server Error {str(e)}")
