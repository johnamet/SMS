#!/usr/bin/python3
"""
The script defines the database storage class.
"""
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, scoped_session

from models.announcement import Announcement
from models.attendance import Attendance
from models.basemodel import Base
from models.basemodel import BaseModel
from models.classe import Class
from models.course import Course
from models.feedback import Feedback
from models.grade import Grade
from models.parent import Parent
from models.permission import Permission
from models.staff import Staff
from models.student import Student
from models.user import User

# Dictionary to map class names to actual class objects
classes = {"BaseModel": BaseModel, "User": User,
           "Course": Course, "Announcement": Announcement,
           "Feedbacks": Feedback, "Student": Student, "Parent": Parent,
           "Staff": Staff, "Gradebook": Grade, "Permission": Permission,
           "Attendance": Attendance, "Class": Class}


class DBStorage:
    """
    The database storage class.
    """

    def __init__(self):
        """
        Initialise the database storage class.
        """
        try:
            if environ.get("STORAGE_ENGINE") == "db":
                self.__user = environ["STORAGE_USER"]
                self.__password = environ["STORAGE_PASSWORD"]
                self.__database = environ["STORAGE_DATABASE"]
                self.__host = environ["STORAGE_HOST"]

                # Create the engine with connection pool
                self.__engine = create_engine(
                    f'mysql+mysqldb://{self.__user}:{self.__password}@{self.__host}/{self.__database}',
                    poolclass=QueuePool,
                    pool_size=5,
                    pool_pre_ping=True,  # Optional
                )

                # Create session factory
                session_factory = sessionmaker(bind=self.__engine)
                self.__Session = scoped_session(session_factory)

                # Create a new session
                self.__session = self.__Session()

                # Drop all tables if running in test environment
                if environ.get("SMS_ENV") == "test":
                    Base.metadata.drop_all(self.__engine)

                # Create all tables
                Base.metadata.create_all(self.__engine)
        except KeyError as e:
            raise ValueError(f"Missing environment variable: {e}")
        except Exception as e:
            raise e

    def all(self, cls=None):
        """
        Query all records in the database.
        Args:
            cls (class, optional): filter query to return objects of this class. Defaults to None.
        Returns:
            dict: all records in the database.
        """
        all_rows = {}

        if cls is None:
            for class_name, class_obj in classes.items():
                query = self.__session.query(class_obj)
                rows = query.all()
                all_rows.update({f"{class_name}.{row.id}": row for row in rows})
        else:
            rows = self.__session.query(cls).all()
            all_rows.update({f"{cls.__name__}.{row.id}": row for row in rows})

        return all_rows

    def new(self, obj):
        """
        Insert a new record in the database.
        Args:
            obj (object): the record to insert.
        """
        if obj:
            self.__session.add(obj)

        if self.__session.dirty is not None:
            self.save()

    def save(self, obj=None):
        """
        Save all records in the database.
        """
        if obj is not None:
            self.new(obj)

        self.__session.commit()

    def delete(self, obj):
        """
        Delete an object from the database.
        Args:
            obj (object): the object to delete.
        """

        self.__session.delete(obj)
        self.__session.commit()

    def delete_by_id(self, cls, id_):
        """
        Delete an object from the database.
        Args:
            cls (class): the class to delete.
            id_ (str): the id of the object to delete.
        """
        (self.__session.query(cls)
         .filter(cls.id == id_).delete())
        self.__session.commit()

    def reload(self):
        """
        Reload all records in the database.
        """
        self.__session.close()
        self.__session = self.__Session()

    def get_by_id(self, cls, id):
        """
        Get an object from the database.
        Args:
            cls (class): the class to query.
            id (str): the id of the object to get.

        Returns:
            object: an object from the database.
        """
        query = self.__session.query(cls).filter(cls.id == id)
        if query is None:
            return None
        return query.first()

    def query(self, cls):
        """
        Query all records in the database.
        Args:
            cls (class): the class to query.
        """
        return self.__session.query(cls)

    def get_by_filter(self, cls, filter_):
        """
        Get an object from the database.
        Args:
            cls (class): the class to query.
            filter_ (condition): the filter to query.

        Returns:
            object: the filtered object.
        """

        query = self.__session.query(cls).filter(filter_)

        return query

    def close(self):
        """
        Close the database session.
        """
        self.__session.close()


# Instantiate the storage engine
if environ.get("STORAGE_ENGINE") == "db":
    dbstorage = DBStorage()
    dbstorage.reload()
