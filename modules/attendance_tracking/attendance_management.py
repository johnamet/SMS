#!/usr/bin/python3
"""
Attendance management module.

This module provides methods to manage attendance records for students.
"""

from sqlalchemy import desc, asc

from models import storage, Attendance, Class


class AttendanceManagement:
    """
    Attendance management module.

    This module provides methods to manage attendance records for students.

    Attributes:
        academic_year (str): The academic year for attendance records.
        term (str): The term for attendance records.
        class_id (str): The ID of the class for which attendance is managed.
    """

    def __init__(self, academic_year=None, term=None, class_id=None):
        """
        Initialize the AttendanceManagement instance.

        Args:
            academic_year (str): The academic year for attendance records.
            term (str): The term for attendance records.
            class_id (str): The ID of the class for which attendance is managed.
        """
        self.academic_year = academic_year
        self.term = term
        self.class_id = class_id

    def get_attendance(self, **kwargs):
        """
        Get attendance records based on the provided filters.

        Returns:
            tuple: A tuple containing a list of attendance records and a message.
        """
        try:
            query = storage.query(Attendance)
            if self.class_id:
                class_ = storage.get(Class, self.class_id)
                if class_:
                    query = query.filter(Attendance.class_id == class_.id,
                                         Class.academic_year == self.academic_year)
                else:
                    raise ValueError(f"Class with id {self.class_id} was not found.")

            if self.academic_year:
                query = query.filter(Attendance.academic_year == self.academic_year)

            if self.term:
                query = query.filter(Attendance.term == self.term)

            if kwargs and "id" in kwargs:
                query = query.filter(Attendance.id == kwargs["id"])

            if kwargs and "sort" in kwargs:
                if kwargs["sort"] == "asc":
                    query = query.order_by(asc(Attendance.date))
                else:
                    query = query.order_by(desc(Attendance.date))

            attendances = query.all()
            return attendances, "Attendance records fetched successfully."
        except Exception as e:
            return [], f"Failed to fetch attendance records: {str(e)}"

    def get_attendance_by_class_id(self, class_id):
        """
        Get attendance records for a specific class.

        Args:
            class_id (str): The ID of the class.

        Returns:
            tuple: A tuple containing a list of attendance records and a message.
        """
        try:
            attendances = storage.query(Attendance).filter(Attendance.class_id == class_id).all()
            return attendances, "Attendance records fetched successfully."
        except Exception as e:
            return [], f"Failed to fetch attendance records: {str(e)}"

    def get_attendance_by_term(self, term):
        """
        Get attendance records for a specific term.

        Args:
            term (str): The term.

        Returns:
            tuple: A tuple containing a list of attendance records and a message.
        """
        try:
            attendances = storage.query(Attendance).filter(Attendance.term == term).all()
            return attendances, "Attendance records fetched successfully."
        except Exception as e:
            return [], f"Failed to fetch attendance records: {str(e)}"

    def get_student_attendance(self, student_id):
        """
        Get attendance records for a specific student.

        Args:
            student_id (str): The ID of the student.

        Returns:
            tuple: A tuple containing a list of attendance records and a message.
        """
        try:
            attendances = storage.query(Attendance).filter(Attendance.student_id == student_id).all()
            return attendances, "Attendance records fetched successfully."
        except Exception as e:
            return [], f"Failed to fetch attendance records: {str(e)}"

    def create_attendance(self, student_id, status, **kwargs):
        """
        Create a new attendance record.

        Args:
            student_id (str): The ID of the student.
            status (int): The attendance status (1 == 'present' or 0 =='absent').

        Returns:
            tuple: A tuple containing the created attendance record and a message.
        """
        if self.class_id is None or self.academic_year is None or self.term is None:
            raise ValueError("Attendance management module requires class_id, academic_year, and term to be set.")
        try:
            attendance = Attendance(student_id=student_id,
                                    class_id=self.class_id,
                                    academic_year=self.academic_year,
                                    term=self.term,
                                    status=status, **kwargs)
            storage.save(attendance)
            return attendance, "Attendance created successfully"
        except Exception as e:
            return None, f"Failed to create attendance record: {str(e)}"

    def mark_attendance(self, attendances):
        """
        Mark attendance for multiple students.

        Args:
            attendances (list): List of attendance records to mark.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            for attendance in attendances:
                storage.new(attendance)
            return True, "Attendance marked successfully"
        except Exception as e:
            return False, f"Failed to mark attendance: {str(e)}"

    def update_attendance(self, attendance_id, **kwargs):
        """
        Update an existing attendance record.

        Args:
            attendance_id (str): The ID of the attendance record to update.
            **kwargs: Keyword arguments for fields to update.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            attendance = storage.get_by_id(Attendance, attendance_id)
            if attendance:
                attendance.update(**kwargs)
                attendance.save()
                return True, "Attendance updated successfully"
            else:
                return False, "Attendance not found"
        except Exception as e:
            return False, f"Failed to update attendance record: {str(e)}"
