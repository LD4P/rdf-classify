import unittest
from src import data_bunch

class TestDataBunch(unittest.TestCase):

    def setUp(self):
        pass

    def test_has_data_bunch(self):
        assert hasattr(data_bunch, "databunch")
