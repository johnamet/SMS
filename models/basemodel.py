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
    id = uuid4()
    created_at = datetime.now()
    updated_at = datetime.now()

    def __init__(self, *args, **kwargs):
        if kwargs is not None:
            for k, v in kwargs.items():
                if k != "id":
                    setattr(self, k, v)
        else:
            self.created_at = BaseModel.created_at
            self.updated_at = BaseModel.updated_at
            self.id = BaseModel.id

    def __repr__(self):
        """
        The representation of the model
        """
        return f"<{self.__class__.__name__}.{self.id}>: {self.__dict__}"

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

        setattr(self, "updated_at", datetime.now())

    def serialize(self):
        """
        The method to serialize a model
        """

        self.__dict__["key"] = f"{self.__class__.__name__}.{self.id}"
        return self.__dict__
