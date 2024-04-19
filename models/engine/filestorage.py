import os
import json

from models import classes

class FileStorage:
    """
    FileStorage class to handle file storage
    Args:
        __file_storage_path (str): path to file storage
        __storage (str): file storage file
    """

    __file_storage_path = "./.store/"
    __storage = os.path.join(__file_storage_path, "file.json")
    __objs = {}

    def __init__(self):
        if not os.path.isfile(self.__storage):
            try:
                os.makedirs(self.__file_storage_path)
            except FileExistsError:
                pass

    def all(self):
        return self.__objs

    def new(self, obj):
        """
        Add a new obj to storage
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objs[key] = obj

    def __serialize(self):
        objs_s = {}
        for key, obj in self.__objs.items():
            objs_s[key] = obj.serialize()
        return objs_s

    def __deserialize(self, data):
        cls = classes[data['__class__']]
        for key, obj_data in data.items():
            self.__objs[key] = cls(**obj_data)

    def save(self):
        serialized_obj = self.__serialize()
        with open(self.__storage, "w") as file:
            json.dump(serialized_obj, file)

    def reload(self):
        try:
            with open(self.__storage, "r") as file:
                data = json.load(file)
                self.__deserialize(data)
        except FileNotFoundError:
            pass
