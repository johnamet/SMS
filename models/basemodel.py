#!/usr/bin/python3
"""
The base for all models
"""
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """
    The base of all the models
    Attributes:
        id (UUID): the id of the model
        created_at (datetime): the creation time of the model
        updated_at (datetime): the last update time of the model
    """

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id", str(uuid4()))
        self.created_at = kwargs.get("created_at", datetime.now())
        self.updated_at = kwargs.get("updated_at", datetime.now())
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """
        The representation of the model
        """
        return f"<{self.__class__.__name__}.{self.id}>: {self.__dict__}"

    def delete(self):
        """
        The method to delete a model
        """
        pass

    def update(self, **kwargs):
        """
        The method to update a model
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()

    def serialize(self):
        """
        The method to serialize a model
        """
        obj_s = self.__dict__.copy()
        obj_s["created_at"] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        obj_s["updated_at"] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        obj_s["__class__"] = self.__class__.__name__
        return obj_s

    @classmethod
    def deserialize(cls, obj):
        obj["created_at"] = datetime.strptime(obj["created_at"], "%Y-%m-%d %H:%M:%S")
        obj["updated_at"] = datetime.strptime(obj["updated_at"], "%Y-%m-%d %H:%M:%S")
        instance = cls(**obj)
        return instance
