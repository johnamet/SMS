#!/usr/bin/python3

"""
The base for all models
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    The base of all the models

    Attributes:
        id (UUID): The ID of the model.
        created_at (datetime): The creation time of the model.
        updated_at (datetime): The last update time of the model.
    """

    id = Column(String(50), primary_key=True, default=str(uuid4))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize a BaseModel instance.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.id = kwargs.get("id", str(uuid4()))
        self.created_at = kwargs.get("created_at", datetime.now())
        self.updated_at = kwargs.get("updated_at", datetime.now())
        for k, v in kwargs.items():
            if k != "__class__":
                setattr(self, k, v)

    def __str__(self):
        """
        Return a string representation of the model.

        Returns:
            str: String representation of the model.
        """
        return f"<{self.__class__.__name__}.{self.id}>: {self.__dict__}"

    def delete(self):
        """
        Delete the model.
        """
        pass

    def update(self, **kwargs):
        """
        Update the model.

        Args:
            **kwargs: Key-value pairs of attributes to update.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()

    def serialize(self):
        """
        Serialize the model.

        Returns:
            dict: Serialized representation of the model.
        """
        obj_s = self.__dict__.copy()
        if "_sa_instance_state" in obj_s: del obj_s["_sa_instance_state"]
        if type(obj_s["created_at"]) == datetime:
            obj_s["created_at"] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if type(obj_s["updated_at"]) == datetime:
            obj_s["updated_at"] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        for k, v in obj_s.items():
            if isinstance(v, BaseModel):
                obj_s[k] = v.serialize()

        obj_s["__class__"] = self.__class__.__name__
        return obj_s

    @classmethod
    def deserialize(cls, obj):
        """
        Deserialize the model.

        Args:
            obj (dict): Serialized representation of the model.

        Returns:
            BaseModel: Deserialized model instance.
        """
        obj["created_at"] = datetime.strptime(obj["created_at"], "%Y-%m-%d %H:%M:%S")
        obj["updated_at"] = datetime.strptime(obj["updated_at"], "%Y-%m-%d %H:%M:%S")
        instance = cls(**obj)
        return instance

    def save(self):
        """
        Save the Model instance to the storage.


        Returns:
            bool: True if successfully scleart
            aved, False otherwise.
        """
        from models import storage
        try:
            storage.save(self)
            return True
        except Exception as e:
            print(f"Error saving Model: {e}")
            return False

