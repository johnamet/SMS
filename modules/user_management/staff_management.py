#!/usr/bin/ptython3
"""
Staff management module
"""
from models.staff import Staff
from models import storage


class StaffManagement:
    """
    Staff management class
    """

    def create_staff(self, staff):
        """
        Creates staff with given staff obj
        Args:
            staff (Staff): Staff obj
        """

        try:
            staff.save()
            return True, "Saved successfully."
        except Exception as e:
            return False, f"Failed to save staff: {e}"

    def delete_staff(self, staff=None, staff_id=None):

        if staff:
            storage.delete(staff)
            return True, "Deleted successfully."
        if staff_id:
            storage.delete_by_id(staff_id)
            return True, "Deleted successfully."

        if staff is None and staff_id is None:
            return False, "No staff or staff id given."

    def update_staff(self, staff=None,
                     staff_id=None, **kwargs):
        """
        Updates staff with given staff obj or id
        """

        try:
            updated_staff = staff.update(**kwargs)

            storage.delete(staff)
            updated_staff.save()

            return updated_staff.id == staff.id, "Staff updated successfully."
        except Exception as e:
            return False, f"Failed to update staff: {e}"


    def get_staff(self, staff_id=None):
        """
        Gets staffs if given staff id get a single staff member
        Args:
            staff_id (str, optional): Staff member id. Defaults to None.
        """

        if staff_id:
            query = storage.get_by_id(Staff, staff_id).first()

            if query:
                return query, "Found Staff member"
            else:
                return None, "Staff member not found"

        query = storage.get_all(Staff)
        if query:
            return query.all(), "Found Staff member"
        else:
            return None, "Staff members not found"

    def get_staff_by_criteria(self, **criteria):
        """
        Retrieve staff members based on specified criteria.

        Args:
            **criteria: Keyword arguments representing the criteria to filter staff members.

        Returns:
            tuple: A tuple containing the retrieved staff members and a message.
        """
        try:
            staff_members = storage.query(Staff).filter_by(**criteria).all()
            if staff_members:
                return staff_members, "Staff members found."
            else:
                return None, "No staff members found matching the criteria."
        except Exception as e:
            return None, f"Failed to retrieve staff members: {e}"




