#!/usr/bin/python3
"""
The base for all models
"""
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """
    The base of all the models
    """

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.id = str(uuid4())

    def __repr__(self):
        """
        The representation of the model
        """
        return f"<{self.__class__.__name__}: {self.id}>"

    def __str__(self):
        """
        The representation of the model
        """
        return f"<{self.__class__.__name__}: {self.id}>"

    def new(self):
        """
        The method to create a new model
        """
        pass

    def delete(self):
        """
        The method to delete a model
        """
        pass

    def update(self):
        """
        The method to update a model
        """
        pass

    def serialize(self):
        """
        The method to serialize a model
        """
        pass

    def deserialize(self):
        """
        The method to deserialize a model
        """
        self.__dict__["key"] = f"{self.__class__.__name__}.{self.id}"
        return self.__dict__
