import unittest

from models.basemodel import BaseModel


class BaseModelTestCase(unittest.TestCase):
    def test_basemodel(self):
        basemodel = BaseModel()
        self.assertTrue(basemodel is not None)

    def test_basemodel_id(self):
        basemodel = BaseModel()
        self.assertTrue(basemodel.id is not None)

    def test_basemodel_name(self):
        basemodel = BaseModel()
        basemodel.name = "BaseModel"
        self.assertTrue(basemodel.name is not None)

    def test_basemodel_repr(self):
        basemodel = BaseModel()
        self.assertTrue(str(basemodel) == f"<{basemodel.__class__.__name__}.{basemodel.id}>: {basemodel.__dict__}")

    def test_serialize(self):
        basemodel = BaseModel()
        serialized = basemodel.serialize()
        self.assertTrue(isinstance(serialized, dict))


if __name__ == '__main__':
    unittest.main()
