import unittest
from src import data_prep


class TestDataPrep(unittest.TestCase):

    def setUp(self):
        pass

    def test_has_data_bunch(self):
        assert hasattr(data_prep, "databunch")
